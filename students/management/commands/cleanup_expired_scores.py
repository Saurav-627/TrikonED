"""
Django management command to clean up expired test scores.
Run this command periodically (e.g., daily via cron) to remove expired test scores.

Usage:
    python manage.py cleanup_expired_scores
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from students.models import StudentTestScore


class Command(BaseCommand):
    help = 'Delete expired English proficiency test scores'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        today = timezone.now().date()
        dry_run = options['dry_run']

        # Find all expired test scores
        expired_scores = StudentTestScore.objects.filter(
            expiry_date__lt=today
        )

        count = expired_scores.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No expired test scores found.'))
            return

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} expired test score(s):'
                )
            )
            for score in expired_scores:
                self.stdout.write(
                    f'  - {score.student.username}: {score.test_type} '
                    f'(expired on {score.expiry_date})'
                )
        else:
            # Delete expired scores
            deleted_count, _ = expired_scores.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_count} expired test score(s).'
                )
            )
