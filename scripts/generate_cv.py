from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "zar-hlei-sang-cv.pdf"
PORTFOLIO_COPY = ROOT / "assets" / "documents" / "Zar-Hlei-Sang-CV.pdf"

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_X = 18 * mm
MARGIN_TOP = 15 * mm
MARGIN_BOTTOM = 14 * mm

NAVY = colors.HexColor("#10243E")
BLUE = colors.HexColor("#2563EB")
BLUE_PALE = colors.HexColor("#EAF1FF")
SLATE = colors.HexColor("#526177")
LIGHT = colors.HexColor("#DFE6EF")
WHITE = colors.white


def register_fonts():
    regular_candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    bold_candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]

    regular = next((Path(p) for p in regular_candidates if Path(p).exists()), None)
    bold = next((Path(p) for p in bold_candidates if Path(p).exists()), None)

    if regular and bold:
        pdfmetrics.registerFont(TTFont("CVSans", str(regular)))
        pdfmetrics.registerFont(TTFont("CVSans-Bold", str(bold)))
        return "CVSans", "CVSans-Bold"

    return "Helvetica", "Helvetica-Bold"


REGULAR_FONT, BOLD_FONT = register_fonts()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CVName",
        parent=styles["Normal"],
        fontName=BOLD_FONT,
        fontSize=25,
        leading=28,
        textColor=WHITE,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="CVTitle",
        parent=styles["Normal"],
        fontName=REGULAR_FONT,
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#C9D7E8"),
    )
)
styles.add(
    ParagraphStyle(
        name="CVContact",
        parent=styles["Normal"],
        fontName=REGULAR_FONT,
        fontSize=8.2,
        leading=12,
        textColor=WHITE,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="CVSection",
        parent=styles["Normal"],
        fontName=BOLD_FONT,
        fontSize=9.5,
        leading=12,
        textColor=BLUE,
        spaceBefore=7,
        spaceAfter=5,
        uppercase=True,
        tracking=1.1,
    )
)
styles.add(
    ParagraphStyle(
        name="CVBody",
        parent=styles["Normal"],
        fontName=REGULAR_FONT,
        fontSize=8.7,
        leading=12.2,
        textColor=SLATE,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="CVBodyDark",
        parent=styles["CVBody"],
        textColor=NAVY,
    )
)
styles.add(
    ParagraphStyle(
        name="CVRole",
        parent=styles["Normal"],
        fontName=BOLD_FONT,
        fontSize=10.2,
        leading=13,
        textColor=NAVY,
        spaceAfter=1,
    )
)
styles.add(
    ParagraphStyle(
        name="CVMeta",
        parent=styles["Normal"],
        fontName=REGULAR_FONT,
        fontSize=8,
        leading=11,
        textColor=BLUE,
    )
)
styles.add(
    ParagraphStyle(
        name="CVBullet",
        parent=styles["CVBody"],
        leftIndent=10,
        firstLineIndent=-7,
        bulletIndent=0,
        spaceAfter=2.5,
    )
)
styles.add(
    ParagraphStyle(
        name="CVProject",
        parent=styles["Normal"],
        fontName=BOLD_FONT,
        fontSize=9.6,
        leading=12,
        textColor=NAVY,
        spaceAfter=1,
    )
)
styles.add(
    ParagraphStyle(
        name="CVTag",
        parent=styles["Normal"],
        fontName=BOLD_FONT,
        fontSize=7.6,
        leading=10,
        textColor=BLUE,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="CVFooter",
        parent=styles["Normal"],
        fontName=REGULAR_FONT,
        fontSize=7.2,
        textColor=SLATE,
        alignment=TA_CENTER,
    )
)


def section(title):
    return [
        Spacer(1, 2 * mm),
        Paragraph(title.upper(), styles["CVSection"]),
        HRFlowable(width="100%", thickness=0.7, color=LIGHT, spaceAfter=5),
    ]


def bullet(text):
    return Paragraph(f"<bullet>&#8226;</bullet>{text}", styles["CVBullet"])


def role_header(title, organization, dates, location=None):
    left = Paragraph(
        f"<font name='{BOLD_FONT}'>{title}</font><br/>"
        f"<font color='#526177'>{organization}</font>",
        styles["CVRole"],
    )
    location_line = f"<br/><font color='#526177'>{location}</font>" if location else ""
    right = Paragraph(f"<b>{dates}</b>{location_line}", styles["CVMeta"])
    table = Table([[left, right]], colWidths=[126 * mm, 34 * mm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def project(title, status, description, technologies, repo, highlights):
    title_row = Table(
        [[Paragraph(title, styles["CVProject"]), Paragraph(status, styles["CVMeta"])]],
        colWidths=[126 * mm, 34 * mm],
    )
    title_row.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    content = [
        title_row,
        Paragraph(description, styles["CVBody"]),
    ]
    for item in highlights:
        content.append(bullet(item))
    content.append(
        Paragraph(
            f"<b>Stack:</b> {technologies} &nbsp;&nbsp; <link href='{repo}' color='#2563EB'>GitHub repository</link>",
            styles["CVBody"],
        )
    )
    content.append(Spacer(1, 2.2 * mm))
    return KeepTogether(content)


def draw_header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_HEIGHT - 42 * mm, PAGE_WIDTH, 42 * mm, fill=1, stroke=0)

    left = MARGIN_X
    top = PAGE_HEIGHT - 14 * mm
    canvas.setFillColor(WHITE)
    canvas.setFont(BOLD_FONT, 24)
    canvas.drawString(left, top, "Zar Hlei Sang")
    canvas.setFillColor(colors.HexColor("#C9D7E8"))
    canvas.setFont(REGULAR_FONT, 10)
    canvas.drawString(left, top - 7 * mm, "Frontend & Full-Stack Web Developer")

    canvas.setFillColor(WHITE)
    canvas.setFont(REGULAR_FONT, 7.8)
    contact_x = PAGE_WIDTH - MARGIN_X
    lines = [
        "Fuerstenfeldbruck, Germany",
        "+49 151 62616360  |  zarhleisang96@gmail.com",
        "github.com/BenRoSang  |  linkedin.com/in/zar-hlei-sang-b880b4356",
    ]
    for index, line in enumerate(lines):
        canvas.drawRightString(contact_x, top - index * 5.2 * mm, line)

    canvas.setFillColor(SLATE)
    canvas.setFont(REGULAR_FONT, 7.2)
    canvas.drawCentredString(PAGE_WIDTH / 2, 7.5 * mm, f"Zar Hlei Sang  |  Page {doc.page}")
    canvas.restoreState()


def build_cv():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_COPY.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=MARGIN_X,
        leftMargin=MARGIN_X,
        topMargin=49 * mm,
        bottomMargin=MARGIN_BOTTOM,
        title="Zar Hlei Sang - Frontend and Full-Stack Web Developer CV",
        author="Zar Hlei Sang",
        subject="Curriculum Vitae",
    )

    story = []

    story.extend(section("Professional Profile"))
    story.append(
        Paragraph(
            "Frontend and full-stack web developer with three years of professional experience building responsive web applications with JavaScript and PHP. Experienced in React interfaces, REST APIs, Node.js and Express backends, authentication, and relational databases. Based near Munich and seeking a junior frontend, full-stack, or web developer role in Germany. Open to remote, hybrid, and on-site opportunities.",
            styles["CVBodyDark"],
        )
    )

    story.extend(section("Technical Skills"))
    skill_rows = [
        ["Frontend", "HTML5, CSS3, JavaScript (ES6+), TypeScript, React, Next.js, Tailwind CSS, Bootstrap"],
        ["Backend", "Node.js, Express.js, PHP, REST APIs, JWT authentication, Python basics"],
        ["Data", "PostgreSQL, MySQL, Prisma ORM, relational database design"],
        ["Tools & practices", "Git, GitHub, Vite, responsive design, accessibility, testing, Agile/Scrum"],
    ]
    skill_table = Table(
        [[Paragraph(f"<b>{label}</b>", styles["CVBodyDark"]), Paragraph(value, styles["CVBody"])] for label, value in skill_rows],
        colWidths=[34 * mm, 126 * mm],
    )
    skill_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BLUE_PALE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(skill_table)

    story.extend(section("Professional Experience"))
    story.append(role_header("Frontend Web Developer", "ZetaSynQ Solutions Co., Ltd.", "01/2020 - 02/2023", "Myanmar"))
    story.extend(
        [
            bullet("Developed and implemented a responsive employee-management web platform."),
            bullet("Built dynamic user interfaces with JavaScript and PHP, translating business requirements into practical workflows."),
            bullet("Integrated REST APIs to load, submit, and manage application data."),
            bullet("Improved usability across screen sizes and continuously refined the user experience."),
            bullet("Refactored frontend code into clearer, more maintainable structures and collaborated in an Agile environment."),
        ]
    )

    story.extend(section("Selected Projects"))
    story.append(
        project(
            "Siang Photography Booking Platform",
            "Full-stack",
            "Business booking platform combining a polished public website with a protected administration area.",
            "React, Tailwind CSS, Node.js, Express, PostgreSQL, JWT",
            "https://github.com/BenRoSang/siang-photography",
            [
                "Created booking, pricing, portfolio, and contact workflows connected to a live REST API.",
                "Built admin tools for bookings, customers, packages, images, payments, and delivery status.",
            ],
        )
    )
    story.append(
        project(
            "Online School Platform",
            "Full-stack MVP",
            "Role-based learning platform where teachers publish courses and students enrol, study, and track progress.",
            "React, TypeScript, Express, Prisma, PostgreSQL, Vitest",
            "https://github.com/BenRoSang/online-school-platform",
            [
                "Implemented secure student and teacher workflows with access and refresh-token authentication.",
                "Added course management, curriculum editing, lesson access, dashboards, progress tracking, and automated tests.",
            ],
        )
    )

    story.append(PageBreak())

    story.extend(section("Selected Projects - Continued"))
    story.append(
        project(
            "Cryptoverse",
            "Frontend",
            "Cryptocurrency dashboard for market statistics, ranked currencies, price history, exchanges, and news.",
            "React, Redux Toolkit, REST APIs, Chart.js, Ant Design",
            "https://github.com/BenRoSang/cryptoverse",
            [
                "Integrated third-party APIs and centralized application state with Redux Toolkit.",
                "Presented live market data through searchable lists, detail views, and charts.",
            ],
        )
    )
    story.append(
        project(
            "Car Rental Service",
            "Work in progress",
            "Responsive vehicle discovery and booking experience with authentication and CMS-managed car data.",
            "Next.js, TypeScript, Tailwind CSS, Clerk, GraphQL, Hygraph",
            "https://github.com/BenRoSang/Car-Rental-Service",
            [
                "Developed vehicle catalogue, search, rental-date selection, and responsive layouts.",
                "Integrated Clerk authentication and GraphQL content from Hygraph.",
            ],
        )
    )

    story.extend(section("Education"))
    story.append(role_header("Bachelor of Engineering (Electronics)", "Kalay Technological University", "12/2011 - 08/2018", "Myanmar"))
    story.append(
        Paragraph(
            "Engineering degree with a strong foundation in analytical thinking, structured problem-solving, and technical systems.",
            styles["CVBody"],
        )
    )

    story.extend(section("Certificates & Training"))
    certificate_rows = [
        ["Advanced Web Development Course", "ICTTI"],
        ["PHP Web Developer Bootcamp", "Myanmar IT Consulting"],
    ]
    certificate_table = Table(
        [[Paragraph(f"<b>{course}</b>", styles["CVBodyDark"]), Paragraph(provider, styles["CVBody"])] for course, provider in certificate_rows],
        colWidths=[100 * mm, 60 * mm],
    )
    certificate_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, LIGHT),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(certificate_table)

    story.extend(section("Languages"))
    language_rows = [
        [Paragraph("<b>Burmese</b><br/><font color='#526177'>Native</font>", styles["CVBodyDark"]),
         Paragraph("<b>English</b><br/><font color='#526177'>Professional working proficiency</font>", styles["CVBodyDark"]),
         Paragraph("<b>German</b><br/><font color='#526177'>B1 - Intermediate</font>", styles["CVBodyDark"])],
    ]
    language_table = Table(language_rows, colWidths=[53.3 * mm, 53.3 * mm, 53.3 * mm])
    language_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7F9FC")),
                ("BOX", (0, 0), (-1, -1), 0.4, LIGHT),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LIGHT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(language_table)

    story.extend(section("Additional Information"))
    story.append(
        Paragraph(
            "Based in Fuerstenfeldbruck in the Munich metropolitan area. Open to remote, hybrid, and on-site junior frontend, full-stack, and web developer positions.",
            styles["CVBody"],
        )
    )

    document.build(story, onFirstPage=draw_header, onLaterPages=draw_header)
    PORTFOLIO_COPY.write_bytes(OUTPUT.read_bytes())


if __name__ == "__main__":
    build_cv()
    print(OUTPUT)
    print(PORTFOLIO_COPY)
