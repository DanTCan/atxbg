import datetime
from django.utils import timezone as django_utils_timezone
from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.search import index


# Create your models here.
class GenresOrderable(Orderable):
    page = ParentalKey('games.GamePage', related_name='genres')
    genre = models.ForeignKey(
        'games.Genre',
        on_delete=models.CASCADE
    )

    panels = [
        SnippetChooserPanel('genre')
    ]


@register_snippet
class Genre(models.Model):
    url = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=30)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('url'),
                FieldPanel('name')
            ])
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class GamesIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ('games.GamePage',)


class GamePage(Page):
    # title = models.CharField(max_length=30)
    # genre = models.ForeignKey(
    #     'games.Genre',
    #     null=True,
    #     blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name='+'
    # )
    # genre = models.ManyToManyField(GenresOrderable, related_name='genres')
    description = models.CharField(max_length=500)
    date_added = models.DateField(default=django_utils_timezone.now)
    min_players = models.IntegerField(default=1)
    max_players = models.IntegerField()
    duration = models.TimeField(null=True)
    complexity = models.FloatField(null=True)
    competitiveness = models.FloatField(null=True)

    # TODO: -Teams, -Roles, -Reviews <- add attributes to model
    # TODO: add edit fields for rest of attributes since these are mostly req fields

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('genres'),
        index.SearchField('description'),
    ]

    content_panels = Page.content_panels + [
        # SnippetChooserPanel('genre'),
        InlinePanel('genres', label='Genre'),  # NEED, first arg must match related_name in Orderable.ParentalKey
        FieldPanel('date_added'),
        FieldPanel('description', classname="full"),
        FieldPanel('min_players'),
        FieldPanel('max_players'),
        FieldPanel('duration'),
        FieldPanel('complexity'),
        FieldPanel('competitiveness'),
    ]


# class GenresIndexPage(Page):
#     intro = RichTextField(blank=True)
#
#     content_panels = Page.content_panels + [
#         FieldPanel('intro', classname='full')
#     ]


# class GenrePage(models.Model):
#     intro = RichTextField(blank=True)
#     page = ParentalKey(GamePage, on_delete=models.CASCADE, related_name=)
#
#     content_panels = Page.content_panels + [
#         FieldPanel('intro', classname="full")
#     ]
