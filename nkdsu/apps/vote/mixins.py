from copy import copy
import datetime

from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import DetailView

from .models import Show
from .utils import memoize


class CurrentShowMixin(object):
    def get_context_data(self):
        context = super(CurrentShowMixin, self).get_context_data()
        context['show'] = Show.current()
        context['show'].tracks_sorted_by_votes()  # XXX
        return context


class ShowDetail(DetailView):
    """
    A view that will find a show for any date in the past, redirect to the
    showtime date if necessary, and then render a view with the correct show
    in context.
    """

    model = Show

    @memoize
    def get_object(self):
        """
        Get the show relating to self.date or, if self.date is None, the most
        recent complete show.

        Doesn't use Show.at() because I don't want views creating Shows in the
        database.
        """

        if self.date is None:
            qs = self.model.objects.filter(end__lt=timezone.now())
            qs = qs.order_by('-end')
        else:
            qs = self.model.objects.filter(showtime__gt=self.date)
            qs = qs.order_by('showtime')

        if not qs.exists():
            raise Http404

        return qs[0]

    def get(self, request, *args, **kwargs):
        date_fmt = '%Y-%m-%d'
        date_str = kwargs.get('date')

        if date_str is None:
            self.date = None
        else:
            naive_date = datetime.datetime.strptime(kwargs['date'], date_fmt)
            self.date = timezone.make_aware(naive_date,
                                            timezone.get_current_timezone())

        self.object = self.get_object()

        if (
            self.date is not None and
            self.object.showtime.date() == self.date.date()
        ):
            return super(ShowDetail, self).get(request, *args, **kwargs)
        else:
            new_kwargs = copy(kwargs)
            name = ':'.join([request.resolver_match.namespace,
                             request.resolver_match.url_name])
            new_kwargs['date'] = self.object.showtime.date().strftime(date_fmt)
            url = reverse(name, kwargs=new_kwargs)
            return redirect(url)
