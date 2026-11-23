
from django.core.management.base import BaseCommand
from core.models import Service


SERVICES = [
    {
        "title": "Floor & Wall Tiling Works",
        "slug": "floor-wall-tiling-works",
        "short_description": "Professional floor and wall tiling solutions.",
        "description": "Floor and wall tiling works for interior and property improvement requirements.",
        "icon": "◈",
        "order": 1,
    },
    {
        "title": "Floor & Wall Marble Works",
        "slug": "floor-wall-marble-works",
        "short_description": "Marble installation and finishing works.",
        "description": "Floor and wall marble works with attention to alignment, finishing and detail.",
        "icon": "◇",
        "order": 2,
    },
    {
        "title": "Kitchen Top, Reception Area & Counter",
        "slug": "kitchen-reception-counter-works",
        "short_description": "Custom kitchen tops, reception areas and counters.",
        "description": "Installation and improvement works for kitchen tops, reception areas and counters.",
        "icon": "▱",
        "order": 3,
    },
    {
        "title": "Dry Cladding",
        "slug": "dry-cladding",
        "short_description": "Professional dry cladding installation solutions.",
        "description": "Dry cladding works for suitable interior and exterior applications.",
        "icon": "▥",
        "order": 4,
    },
    {
        "title": "Carpentry & Wood Flooring Works",
        "slug": "carpentry-wood-flooring-works",
        "short_description": "Carpentry solutions and wood flooring works.",
        "description": "Carpentry and wood flooring works for property interiors and improvement projects.",
        "icon": "▤",
        "order": 5,
    },
    {
        "title": "Painting Contracting",
        "slug": "painting-contracting",
        "short_description": "Interior and exterior painting works.",
        "description": "Painting contracting works for residential and commercial properties.",
        "icon": "◫",
        "order": 6,
    },
    {
        "title": "False Ceiling & Light Partitions Installation",
        "slug": "false-ceiling-light-partitions",
        "short_description": "False ceiling and light partition installation.",
        "description": "False ceiling and light partition installation for interior spaces.",
        "icon": "▦",
        "order": 7,
    },
    {
        "title": "Wallpaper Fixing Works",
        "slug": "wallpaper-fixing-works",
        "short_description": "Wallpaper installation and wall finishing.",
        "description": "Wallpaper fixing works to enhance interior spaces.",
        "icon": "▧",
        "order": 8,
    },
    {
        "title": "Plaster Works",
        "slug": "plaster-works",
        "short_description": "Professional plastering and surface preparation.",
        "description": "Plaster works for wall and ceiling surfaces.",
        "icon": "▱",
        "order": 9,
    },
    {
        "title": "Electrical & Lighting Works",
        "slug": "electrical-lighting-works",
        "short_description": "Electrical fittings and lighting installation works.",
        "description": "Electrical and lighting works for property requirements.",
        "icon": "⌁",
        "order": 10,
    },
    {
        "title": "Plumbing Works",
        "slug": "plumbing-works",
        "short_description": "Plumbing installation and maintenance works.",
        "description": "Plumbing works for residential and commercial property requirements.",
        "icon": "⌇",
        "order": 11,
    },
    {
        "title": "General Maintenance Works",
        "slug": "general-maintenance-works",
        "short_description": "General property maintenance solutions.",
        "description": "General maintenance works for property upkeep and improvement requirements.",
        "icon": "⚙",
        "order": 12,
    },
]


class Command(BaseCommand):
    help = "Add the initial BOOM EXPRESS technical services."

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        for item in SERVICES:
            slug = item["slug"]
            service, created = Service.objects.get_or_create(
                slug=slug,
                defaults=item,
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created: {service.title}")
                )
            else:
                existing_count += 1
                self.stdout.write(
                    f"Already exists: {service.title}"
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Finished. Created: {created_count}, "
                f"Already existing: {existing_count}"
            )
        )
