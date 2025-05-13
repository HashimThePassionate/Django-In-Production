from django.core.management.base import BaseCommand
from blog.models import Blog
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Returns the total number of blogs in the database with optional filters'

    def add_arguments(self, parser):
        parser.add_argument(
            '--min-letters',
            type=int,
            help='Filter blogs with minimum letter count',
            default=0
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Display detailed output for each blog'
        )
        parser.add_argument(
            '--start-date',
            type=str,
            help='Filter blogs created after this date (YYYY-MM-DD)'
        )
        parser.add_argument(
            '--end-date',
            type=str,
            help='Filter blogs created before this date (YYYY-MM-DD)'
        )

    def handle(self, *args, **kwargs):
        min_letters = kwargs['min_letters']
        verbose = kwargs['verbose']
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')

        try:
            # QuerySet banane ke liye initial filter
            queryset = Blog.objects.all()

            # Letter count filter (dynamic method se)
            if min_letters > 0:
                queryset = queryset.filter(id__in=[blog.id for blog in queryset if self.get_letter_count(blog) >= min_letters])

            # Date range filter
            if start_date:
                queryset = queryset.filter(created_at__gte=timezone.datetime.strptime(start_date, '%Y-%m-%d'))
            if end_date:
                queryset = queryset.filter(created_at__lte=timezone.datetime.strptime(end_date, '%Y-%m-%d') + timezone.timedelta(days=1))

            total_blogs = queryset.count()
            blogs = queryset.all()

            if blogs.exists():
                if verbose:
                    self.stdout.write(self.style.SUCCESS('Detailed Blog List:'))
                    for blog in blogs:
                        letter_count = self.get_letter_count(blog)
                        self.stdout.write(self.style.SUCCESS(
                            f'- Title: "{blog.title}", Created: {blog.created_at}, Letters: {letter_count}, Author: {blog.author_full_name or "Unknown"}'
                        ))
                self.stdout.write(self.style.SUCCESS(f'Total number of blogs: "{total_blogs}"'))
            else:
                self.stdout.write(self.style.WARNING('No blogs found matching the criteria.'))

        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Invalid date format. Use YYYY-MM-DD. Error: {e}'))
        except ObjectDoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Database error: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))

    def get_letter_count(self, blog):
        # Dynamic letter count calculation from content
        return sum(1 for c in (blog.content or '') if c.isalpha())

# Note: Ensure 'created_at' and 'author_full_name' are available in your Blog model.
# If 'author_full_name' is not a method, adjust the call accordingly.