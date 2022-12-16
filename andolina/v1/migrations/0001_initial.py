# Generated by Django 4.1.2 on 2022-12-15 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="name of the activity", max_length=100, null=True
                    ),
                ),
                (
                    "nb_places_available",
                    models.PositiveSmallIntegerField(blank=True, null=True),
                ),
                (
                    "is_inscription_open",
                    models.BooleanField(blank=True, default=True, null=True),
                ),
                (
                    "is_all_year",
                    models.BooleanField(blank=True, default=True, null=True),
                ),
                (
                    "date",
                    models.DateField(
                        blank=True,
                        help_text="date of the activity if it is not perform all year",
                        null=True,
                    ),
                ),
                (
                    "days_hour",
                    models.CharField(
                        blank=True,
                        help_text="format: day1/start_hour-stop_hour, day2/hours example: Monday/15:30-16:30, Wednesday/15:30-16:30",
                        max_length=40,
                        null=True,
                    ),
                ),
                (
                    "details",
                    models.TextField(
                        blank=True,
                        help_text="Explain to parents what is this activity",
                        null=True,
                    ),
                ),
                (
                    "price",
                    models.CharField(
                        choices=[
                            ("daily_price", "daily price"),
                            ("monthly_price", "monthly price"),
                        ],
                        default="monthly_price",
                        max_length=40,
                        null=True,
                    ),
                ),
                ("price_per_day", models.FloatField(blank=True, null=True)),
                ("price_per_month", models.FloatField(blank=True, null=True)),
                ("money_earned_by_school", models.FloatField(blank=True, null=True)),
                (
                    "public",
                    models.CharField(
                        choices=[("children", "children"), ("parents", "parents")],
                        max_length=40,
                        null=True,
                    ),
                ),
                ("comment_for_parent", models.TextField(blank=True, null=True)),
                (
                    "edit_permission",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Creator only", "Creator only"),
                            ("Group only", "Group only"),
                            ("Several groups", "Several groups"),
                            ("All", "All"),
                        ],
                        max_length=40,
                        null=True,
                    ),
                ),
                (
                    "ask_inscription",
                    models.ManyToManyField(
                        related_name="inscriptions", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        blank=True,
                        help_text="Adult in charge",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activity",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "users",
                    models.ManyToManyField(
                        blank=True,
                        related_name="activities",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Activities",
                "ordering": ["name", "public", "is_inscription_open"],
            },
        ),
        migrations.CreateModel(
            name="Archive",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="name of the activity", max_length=100, null=True
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True, choices=[("bill", "bill")], max_length=40, null=True
                    ),
                ),
                (
                    "year",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (2022, 2022),
                            (2023, 2023),
                            (2024, 2024),
                            (2025, 2025),
                            (2026, 2026),
                            (2027, 2027),
                            (2028, 2028),
                            (2029, 2029),
                            (2030, 2030),
                            (2031, 2031),
                            (2032, 2032),
                            (2033, 2033),
                            (2034, 2034),
                            (2035, 2035),
                            (2036, 2036),
                            (2037, 2037),
                            (2038, 2038),
                            (2039, 2039),
                            (2040, 2040),
                            (2041, 2041),
                            (2042, 2042),
                            (2043, 2043),
                            (2044, 2044),
                            (2045, 2045),
                            (2046, 2046),
                            (2047, 2047),
                            (2048, 2048),
                            (2049, 2049),
                            (2050, 2050),
                            (2051, 2051),
                            (2052, 2052),
                            (2053, 2053),
                            (2054, 2054),
                            (2055, 2055),
                            (2056, 2056),
                            (2057, 2057),
                            (2058, 2058),
                            (2059, 2059),
                            (2060, 2060),
                            (2061, 2061),
                            (2062, 2062),
                            (2063, 2063),
                            (2064, 2064),
                            (2065, 2065),
                            (2066, 2066),
                            (2067, 2067),
                            (2068, 2068),
                            (2069, 2069),
                            (2070, 2070),
                            (2071, 2071),
                            (2072, 2072),
                            (2073, 2073),
                            (2074, 2074),
                            (2075, 2075),
                            (2076, 2076),
                            (2077, 2077),
                            (2078, 2078),
                            (2079, 2079),
                            (2080, 2080),
                            (2081, 2081),
                            (2082, 2082),
                            (2083, 2083),
                            (2084, 2084),
                            (2085, 2085),
                            (2086, 2086),
                            (2087, 2087),
                            (2088, 2088),
                            (2089, 2089),
                            (2090, 2090),
                            (2091, 2091),
                            (2092, 2092),
                            (2093, 2093),
                            (2094, 2094),
                            (2095, 2095),
                            (2096, 2096),
                            (2097, 2097),
                            (2098, 2098),
                            (2099, 2099),
                            (2100, 2100),
                            (2101, 2101),
                            (2102, 2102),
                            (2103, 2103),
                            (2104, 2104),
                            (2105, 2105),
                            (2106, 2106),
                            (2107, 2107),
                            (2108, 2108),
                            (2109, 2109),
                            (2110, 2110),
                            (2111, 2111),
                            (2112, 2112),
                            (2113, 2113),
                            (2114, 2114),
                            (2115, 2115),
                            (2116, 2116),
                            (2117, 2117),
                            (2118, 2118),
                            (2119, 2119),
                            (2120, 2120),
                            (2121, 2121),
                        ],
                        null=True,
                    ),
                ),
                (
                    "month",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                            (9, 9),
                            (10, 10),
                            (11, 11),
                            (12, 12),
                        ],
                        null=True,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Archives",
                "ordering": ["type", "year", "month", "name"],
            },
        ),
        migrations.CreateModel(
            name="Child",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("birth_date", models.DateField(blank=True, null=True)),
                ("age", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("date_created", models.DateField(auto_now_add=True)),
                ("date_updated", models.DateField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Children",
                "ordering": ["user__last_name", "user__first_name"],
            },
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("mobile", models.CharField(blank=True, max_length=20, null=True)),
                ("address", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "school_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "bank_account",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teacher",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Teachers",
                "ordering": ["user__last_name", "user__first_name"],
            },
        ),
        migrations.CreateModel(
            name="Sheet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "year",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (2022, "2022"),
                            (2023, "2023"),
                            (2024, "2024"),
                            (2025, "2025"),
                            (2026, "2026"),
                            (2027, "2027"),
                            (2028, "2028"),
                            (2029, "2029"),
                            (2030, "2030"),
                            (2031, "2031"),
                            (2032, "2032"),
                            (2033, "2033"),
                            (2034, "2034"),
                            (2035, "2035"),
                            (2036, "2036"),
                            (2037, "2037"),
                            (2038, "2038"),
                            (2039, "2039"),
                            (2040, "2040"),
                            (2041, "2041"),
                            (2042, "2042"),
                            (2043, "2043"),
                            (2044, "2044"),
                            (2045, "2045"),
                            (2046, "2046"),
                            (2047, "2047"),
                            (2048, "2048"),
                            (2049, "2049"),
                            (2050, "2050"),
                            (2051, "2051"),
                            (2052, "2052"),
                            (2053, "2053"),
                            (2054, "2054"),
                            (2055, "2055"),
                            (2056, "2056"),
                            (2057, "2057"),
                            (2058, "2058"),
                            (2059, "2059"),
                            (2060, "2060"),
                            (2061, "2061"),
                            (2062, "2062"),
                            (2063, "2063"),
                            (2064, "2064"),
                            (2065, "2065"),
                            (2066, "2066"),
                            (2067, "2067"),
                            (2068, "2068"),
                            (2069, "2069"),
                            (2070, "2070"),
                            (2071, "2071"),
                            (2072, "2072"),
                            (2073, "2073"),
                            (2074, "2074"),
                            (2075, "2075"),
                            (2076, "2076"),
                            (2077, "2077"),
                            (2078, "2078"),
                            (2079, "2079"),
                            (2080, "2080"),
                            (2081, "2081"),
                            (2082, "2082"),
                            (2083, "2083"),
                            (2084, "2084"),
                            (2085, "2085"),
                            (2086, "2086"),
                            (2087, "2087"),
                            (2088, "2088"),
                            (2089, "2089"),
                            (2090, "2090"),
                            (2091, "2091"),
                            (2092, "2092"),
                            (2093, "2093"),
                            (2094, "2094"),
                            (2095, "2095"),
                            (2096, "2096"),
                            (2097, "2097"),
                            (2098, "2098"),
                            (2099, "2099"),
                            (2100, "2100"),
                            (2101, "2101"),
                            (2102, "2102"),
                            (2103, "2103"),
                            (2104, "2104"),
                            (2105, "2105"),
                            (2106, "2106"),
                            (2107, "2107"),
                            (2108, "2108"),
                            (2109, "2109"),
                            (2110, "2110"),
                            (2111, "2111"),
                            (2112, "2112"),
                            (2113, "2113"),
                            (2114, "2114"),
                            (2115, "2115"),
                            (2116, "2116"),
                            (2117, "2117"),
                            (2118, "2118"),
                            (2119, "2119"),
                            (2120, "2120"),
                            (2121, "2121"),
                        ],
                        null=True,
                    ),
                ),
                (
                    "month",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        choices=[
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                            (6, "6"),
                            (7, "7"),
                            (8, "8"),
                            (9, "9"),
                            (10, "10"),
                            (11, "11"),
                            (12, "12"),
                        ],
                        null=True,
                    ),
                ),
                ("content", models.JSONField()),
                ("is_archived", models.BooleanField(default=False, null=True)),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sheet",
                        to="v1.activity",
                    ),
                ),
                (
                    "archive",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sheets",
                        to="v1.archive",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Sheets",
                "ordering": ["activity", "year", "month"],
            },
        ),
        migrations.CreateModel(
            name="Parent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("mobile", models.CharField(blank=True, max_length=20, null=True)),
                ("address", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "school_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("socio", "socio"),
                            ("pre socio", "pre socio"),
                            ("collaborador", "collaborador"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "school_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("nif", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "bank_account",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "is_paying_bills",
                    models.BooleanField(blank=True, default=False, null=True),
                ),
                ("date_start_school", models.DateField(blank=True, null=True)),
                ("date_stop_school", models.DateField(blank=True, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_updated", models.DateTimeField(auto_now=True)),
                (
                    "children",
                    models.ManyToManyField(
                        blank=True, related_name="parent", to="v1.child"
                    ),
                ),
                (
                    "partner",
                    models.ForeignKey(
                        blank=True,
                        help_text="wife/husband of the user",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="v1.parent",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Parents",
                "ordering": ["user__last_name", "user__first_name"],
            },
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("CdT", "CdT"),
                            ("Circulo de familia", "Circulo de familia"),
                            ("Equipo de Docente", "Equipo de Docente"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "leader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group_leader",
                        to="v1.parent",
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(related_name="group", to="v1.parent"),
                ),
                (
                    "representative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group_rep",
                        to="v1.parent",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Groups",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="External",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateField(auto_now_add=True)),
                ("date_updated", models.DateField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Externals",
                "ordering": ["user__last_name", "user__first_name"],
            },
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=50, null=True)),
                ("content", models.JSONField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("BILL", "BILL"),
                            ("INSCRIPTION", "INSCRIPTION"),
                            ("CUOTAS y MATERIAL", "CUOTAS y MATERIAL"),
                            ("COMEDOR", "COMEDOR"),
                            ("ACOMPAÑAMIENTO", "ACOMPAÑAMIENTO"),
                            ("VENTAS", "VENTAS"),
                            ("FORMACIONES", "FORMACIONES"),
                            (
                                "TALLERES, ACTIVIDADES y CAMPAMENTOS",
                                "TALLERES, ACTIVIDADES y CAMPAMENTOS",
                            ),
                            ("EXTRAESCOLARES", "EXTRAESCOLARES"),
                            ("ATENCIÓN TEMPRANA", "ATENCIÓN TEMPRANA"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "type_creation",
                    models.CharField(
                        blank=True,
                        choices=[("manual", "manual"), ("auto", "auto")],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Documents",
                "ordering": ["title"],
            },
        ),
        migrations.AddField(
            model_name="child",
            name="tutor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pupil",
                to="v1.teacher",
            ),
        ),
        migrations.AddField(
            model_name="child",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
