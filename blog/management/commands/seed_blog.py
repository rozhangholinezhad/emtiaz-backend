"""Seed sample categories and posts with cover images (from design)."""
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Category, Post

SAMPLES = [
    {
        "title": "پیش از خرید آپارتمان، چه نکاتی را باید بررسی کنیم؟",
        "excerpt": "از بررسی مدارک و وضعیت سند تا ارزیابی موقعیت، امکانات ساختمان و هزینه‌های جانبی؛ آشنایی با نکات کلیدی می‌تواند به تصمیم‌گیری آگاهانه‌تر در خرید ملک کمک کند.",
        "content": "خرید آپارتمان یکی از مهم‌ترین تصمیم‌های مالی زندگی است.\n\nپیش از امضای هر قراردادی، وضعیت سند، بدهی‌های احتمالی ساختمان، پایان‌کار و انشعابات را بررسی کنید.\n\nموقعیت ملک، دسترسی به خدمات شهری، نورگیری و کیفیت ساخت نیز نقش تعیین‌کننده‌ای در ارزش‌گذاری دارند.",
        "category": "راهنمای خرید ملک",
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuAHdocszdFqbuANN-Lceiw5IClGwASNI7W9QyPDJ6tw3mzPFmWA3JpcVqDsLBYAtCZvYAfhh9IO3Gt0H36JjYRJjo_UeK4UQODwzTWFNJltzuNB2nrCREGB6TWQ3GpuoYT48QkxiWOaiGKRPZskDL7Yw6y40uqT89xFfgZ5mUyNHJWhJUhRP2xu-6c4fiRkTEPUkZd-VEYVTI841ZRDtMVOUzxwy3eZfnDrlTuZCO0sM61oz_kwYG_4IQ",
        "featured": True,
    },
    {
        "title": "راهنمای انتخاب خانه مناسب برای اجاره",
        "excerpt": "برای اجاره خانه، بودجه، دسترسی به محل کار و کیفیت واحد را با دقت بسنجید تا انتخابی پایدار داشته باشید.",
        "content": "در اجاره مسکن، قرارداد شفاف و بررسی وضعیت ملک اهمیت زیادی دارد.\n\nهمسایگی، طبقه، آسانسور، پارکینگ و هزینه‌های شارژ را از قبل استعلام کنید.",
        "category": "رهن و اجاره",
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuA67WESFq1Gl53DgegnY2EEZT8aGoAf4H7fWdBqvi8B41iGWMhfsHk63x56giApKQG-cTGZbrns0IlNBGYW4LzGqhLkbBdUxFyfJZQDelo3paP86s9oPG09jqvOwGKNHntkh6GJsfS5YFAyAIQ-3gbWXq9KxcS3YpYwpS-Fp-hKJvuzqIjlDMwhf7ZGcehiekAOSTAcjT95EMZsQaU_tdGvSQPrKmpPkFlua8tvGkcTwzujtHZWJakODg",
        "featured": False,
    },
    {
        "title": "چه عواملی بر ارزش یک ملک تأثیر می‌گذارند؟",
        "excerpt": "موقعیت جغرافیایی، کاربری، سن بنا و تقاضای منطقه از مهم‌ترین عوامل قیمت‌گذاری ملک هستند.",
        "content": "ارزش ملک تابعی از عرضه و تقاضا، دسترسی‌ها و کیفیت ساخت است.\n\nتغییرات طرح تفصیلی و پروژه‌های عمرانی اطراف نیز می‌تواند قیمت را جابه‌جا کند.",
        "category": "سرمایه‌گذاری",
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuB9jW42DHy2v03Io6momSw-A7gNR_XCPEqgRDfnQqtkMjR8DEtZYRNyaUKBtDQderrKI1tSxMxBEwxM7mEfIgdU1viZENSO3t-BGVU-ZuspgEcTwPxbpteJedzSRmGKggYdCpgA6gmrS1EFT3r4du4lQcZ5-1CuR2om2VdAAZmWLl22gEJpPgvnDAKWiRBkwdbcvAQh28vF_9Wj_7PASjvbBJT6GT3gQqfP0GtonZ3QN1VB1CR6fUudhQ",
        "featured": False,
    },
    {
        "title": "نکات مهم قرارداد اجاره که باید بدانید",
        "excerpt": "مدت قرارداد، مبلغ ودیعه، شرایط فسخ و تعهدات طرفین را با دقت در متن اجاره‌نامه مشخص کنید.",
        "content": "قرارداد اجاره باید شفاف و کامل باشد.\n\nثبت در سامانه املاک و مستغلات و ذکر دقیق مشخصات طرفین ضروری است.",
        "category": "رهن و اجاره",
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuCu4nRr6889_JdL0rqcg9MOrN6LHwSVX8zerWscVIyJrm_6jlhyh-D8WoYxR2alXswjv9aKJS9_s9D6YodhKyGlBshNgMExHAwHmjnMJkTYEZxKNa0ftMoOvd5FVXaLQGTC0M9bWYJKjq_rQjrIr1yQEpg4Pn7EkeuIesfR-Z907N1bNBWrOcYGDP_5RCgYnnbO3fC6WmNCFRRwSmweARJvk61C_RGX0qas60ssRe-2BaPMgT-CvRBxLQ",
        "featured": False,
    },
    {
        "title": "چگونه نور طبیعی، فضای خانه را دلپذیرتر می‌کند؟",
        "excerpt": "نورگیری مناسب، حس فضا و حتی مصرف انرژی را بهبود می‌دهد و در انتخاب ملک نقش مهمی دارد.",
        "content": "جهت ساختمان و ابعاد پنجره‌ها نور طبیعی را تعیین می‌کنند.\n\nدر بازدید حضوری، وضعیت نور را در ساعات مختلف روز بررسی کنید.",
        "category": "طراحی و معماری",
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuBn-EdGC3G3zNU7gl0gPWfqjrh6c0QuV6coICt1mOgBKUCu_33HGVkxSD6HjXZk-7fKmP70LzA2pLBBfiG5alTxpFteVMQ_nbbvgOircjf3mV4Af88tS6abCkGOrVRTcXUWpX6JydYLBLw3JR-4cLch2jey7wKZrdirFQU5lOvHQHm0d4rl-ZS1_V96Y0ITR4RDoy04rYjOjuUqkJZlapL3sNxrL3ZFQ4xLlK9r-803TZ7tUSw39oJGrw",
        "featured": False,
    },
    {
        "title": "پیش از تمدید قرارداد اجاره چه مواردی را بررسی کنیم؟",
        "excerpt": "افزایش اجاره، وضعیت ملک و شرایط جدید بازار را پیش از تمدید ارزیابی کنید.",
        "content": "تمدید اجاره فرصت بازنگری شرایط است.\n\nتعمیرات لازم، مبلغ جدید و مدت قرارداد را شفاف بنویسید.",
        "category": "رهن و اجاره",
        "cover": "https://lh3.googleusercontent.com/aida-public/AB6AXuC3Jr7kDctaIyqtidAZuT1yiNDAne9ePoZlVTJgGSbua3EAbeNg8oj3VCT_HUcJts6-zZu2UkSNzgY0fLEA3bYFBL3Tvh6LxMgGovp_PtwVg9icko4IFadBuUlSypJ1W76b5CN0bRzWGpxeubdiPK9v-JOM_AzehjcGFB96wdrhTomr2z0p8o-ogwuahsH8BRxhblFDphFjfSwmcSUdZQap6z1LtPXbVvStr8mHYu9vwhUo8ZKb6DGRrQ",
        "featured": False,
    },
]


class Command(BaseCommand):
    help = "ایجاد دسته‌ها و مقالات نمونه با تصویر کاور"

    def handle(self, *args, **options):
        created_posts = 0
        for item in SAMPLES:
            cat, _ = Category.objects.get_or_create(
                name=item["category"],
                defaults={"slug": ""},
            )
            post, created = Post.objects.get_or_create(
                title=item["title"],
                defaults={
                    "excerpt": item["excerpt"],
                    "content": item["content"],
                    "cover_image_url": item["cover"],
                    "category": cat,
                    "is_published": True,
                    "is_featured": item["featured"],
                    "published_at": timezone.now(),
                },
            )
            if created:
                created_posts += 1
            else:
                if not post.cover_image_url and not post.cover_image:
                    post.cover_image_url = item["cover"]
                    post.is_published = True
                    post.save(update_fields=["cover_image_url", "is_published"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed کامل شد. مقالات جدید: {created_posts} | کل مقالات: {Post.objects.count()}"
            )
        )
