import uuid
from django.db import models


class Match(models.Model):
    """
    Match models represents match results. Each match contains a start position and an end position
    indicating its location in the sequence

    Matches are associated with one or more SearchTerms through a many-to-many relationship.
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    start = models.IntegerField()
    end = models.IntegerField()

    class Meta:
        ordering = ['start', 'end']

        # we want to avoid storing repeated matched sequence
        constraints = [
            models.UniqueConstraint(fields=["start", "end"], name="unique_match_range")
        ]

    def __str__(self):
        return f"{self.start}-{self.end}"

class SearchTerm(models.Model):
    """
    SearchTerm models represent a valid regex term that was submitted. Each search term associates with
    0 or more matched results
    """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pattern = models.TextField()
    matches = models.ManyToManyField(Match, related_name="search_terms")

    def __str__(self):
        return self.pattern

class Search(models.Model):
    pass
