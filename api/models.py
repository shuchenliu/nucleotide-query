import uuid
from django.db import models
from django.utils import timezone


class Sequence(models.Model):
    """
    Sequence models stores nucleotide sequences. We are dealing with relatively short sequence here so
    in database persistence and retrieval should be ok
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # fields derived from request payload
    nih_db = models.TextField()
    nih_id = models.TextField()
    type = models.TextField()

    # fields derived from response payload
    seqtype = models.TextField()
    accver = models.TextField()
    taxid = models.TextField()
    orgname = models.TextField()
    defline = models.TextField()
    length = models.IntegerField()
    sequence = models.TextField()

    def __str__(self):
        return self.defline

    class Meta:
        # Ensure only one record exists per NIH DB query for a given data type
        constraints = [
            models.UniqueConstraint(fields=["nih_db", "nih_id", "type"], name="unique_sequence_data")
        ]

class Match(models.Model):
    """
    Match models represents match results. Each match contains a start position and an end position
    indicating its location in the sequence

    Matches are associated with one or more SearchTerms through a many-to-many relationship.
    """
    id = models.UUIDField(primary_key=True, editable=False)
    start = models.IntegerField()
    end = models.IntegerField()
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)

    class Meta:
        ordering = ['start', 'end']

        indexes = [
            models.Index(fields=["start", "end", "sequence"]),
        ]

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pattern = models.TextField(unique=True)
    matches = models.ManyToManyField(Match, related_name="search_terms")
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)

    def __str__(self):
        return self.pattern

class Search(models.Model):

    """
    Search model is established in case we want to retrieve most frequent/recent searches.
    Might be good for class-based views with standard CRUD ops, mostly just listing
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    search_term = models.ForeignKey(SearchTerm, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False, db_index=True)

    class Meta:
        ordering = ['created_at']