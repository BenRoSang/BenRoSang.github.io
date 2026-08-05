from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Table, TableStyle

from generate_cv import (
    BOLD_FONT,
    LIGHT,
    MARGIN_BOTTOM,
    MARGIN_X,
    NAVY,
    PAGE_HEIGHT,
    PAGE_WIDTH,
    REGULAR_FONT,
    SLATE,
    WHITE,
    BLUE_PALE,
    bullet,
    project,
    role_header,
    section,
    styles,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "zar-hlei-sang-lebenslauf-de.pdf"
PORTFOLIO_COPY = ROOT / "assets" / "documents" / "Zar-Hlei-Sang-Lebenslauf-DE.pdf"


def draw_header_de(canvas, doc):
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
    canvas.drawString(left, top - 7 * mm, "Frontend- & Full-Stack-Webentwickler")

    canvas.setFillColor(WHITE)
    canvas.setFont(REGULAR_FONT, 7.8)
    contact_x = PAGE_WIDTH - MARGIN_X
    lines = [
        "Fürstenfeldbruck, Deutschland",
        "+49 151 62616360  |  zarhleisang96@gmail.com",
        "github.com/BenRoSang  |  linkedin.com/in/zar-hlei-sang-b880b4356",
    ]
    for index, line in enumerate(lines):
        canvas.drawRightString(contact_x, top - index * 5.2 * mm, line)

    canvas.setFillColor(SLATE)
    canvas.setFont(REGULAR_FONT, 7.2)
    canvas.drawCentredString(PAGE_WIDTH / 2, 7.5 * mm, f"Zar Hlei Sang  |  Seite {doc.page}")
    canvas.restoreState()


def build_cv_de():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    PORTFOLIO_COPY.parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        rightMargin=MARGIN_X,
        leftMargin=MARGIN_X,
        topMargin=49 * mm,
        bottomMargin=MARGIN_BOTTOM,
        title="Zar Hlei Sang - Lebenslauf - Frontend- und Full-Stack-Webentwickler",
        author="Zar Hlei Sang",
        subject="Lebenslauf",
    )

    story = []

    story.extend(section("Kurzprofil"))
    story.append(
        Paragraph(
            "Frontend- und Full-Stack-Webentwickler mit drei Jahren Berufserfahrung in der Entwicklung responsiver Webanwendungen mit JavaScript und PHP. Praxiserfahrung mit React-Oberflächen, REST-APIs, Node.js- und Express-Backends, Authentifizierung sowie relationalen Datenbanken. Wohnhaft im Raum München und auf der Suche nach einer Position als Junior Frontend-, Full-Stack- oder Webentwickler in Deutschland. Offen für Remote-, Hybrid- und Vor-Ort-Arbeit.",
            styles["CVBodyDark"],
        )
    )

    story.extend(section("Technische Kenntnisse"))
    skill_rows = [
        ["Frontend", "HTML5, CSS3, JavaScript (ES6+), TypeScript, React, Next.js, Tailwind CSS, Bootstrap"],
        ["Backend", "Node.js, Express.js, PHP, REST-APIs, JWT-Authentifizierung, Python-Grundkenntnisse"],
        ["Datenbanken", "PostgreSQL, MySQL, Prisma ORM, relationales Datenbankdesign"],
        ["Tools & Methoden", "Git, GitHub, Vite, Responsive Design, Barrierefreiheit, Testing, Agile/Scrum"],
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

    story.extend(section("Berufserfahrung"))
    story.append(role_header("Frontend-Webentwickler", "ZetaSynQ Solutions Co., Ltd.", "01/2020 - 02/2023", "Myanmar"))
    story.extend(
        [
            bullet("Entwicklung und Umsetzung einer responsiven Webplattform für die Mitarbeiterverwaltung."),
            bullet("Programmierung dynamischer Benutzeroberflächen mit JavaScript und PHP sowie Überführung fachlicher Anforderungen in praxistaugliche Abläufe."),
            bullet("Integration von REST-APIs zum Laden, Übermitteln und Verwalten von Anwendungsdaten."),
            bullet("Optimierung der Benutzerfreundlichkeit für verschiedene Bildschirmgrößen und kontinuierliche Verbesserung der User Experience."),
            bullet("Strukturiertes Refactoring für besser wartbaren Frontend-Code und Zusammenarbeit in einem agilen Umfeld."),
        ]
    )

    story.extend(section("Ausgewählte Projekte"))
    story.append(
        project(
            "Siang Photography Booking Platform",
            "Full-Stack",
            "Buchungsplattform für ein Fotografieunternehmen mit moderner öffentlicher Website und geschütztem Administrationsbereich.",
            "React, Tailwind CSS, Node.js, Express, PostgreSQL, JWT",
            "https://github.com/BenRoSang/siang-photography",
            [
                "Entwicklung von Buchungs-, Preis-, Portfolio- und Kontaktfunktionen mit Anbindung an eine REST-API.",
                "Umsetzung von Admin-Funktionen für Buchungen, Kunden, Pakete, Bilder, Zahlungen und Auslieferungsstatus.",
            ],
        )
    )
    story.append(
        project(
            "Online School Platform",
            "Full-Stack-MVP",
            "Rollenbasierte Lernplattform, auf der Lehrkräfte Kurse veröffentlichen und Lernende Kurse belegen sowie ihren Fortschritt verfolgen.",
            "React, TypeScript, Express, Prisma, PostgreSQL, Vitest",
            "https://github.com/BenRoSang/online-school-platform",
            [
                "Implementierung sicherer Abläufe für Lernende und Lehrkräfte mit Access- und Refresh-Token-Authentifizierung.",
                "Entwicklung von Kursverwaltung, Curriculum-Editor, Lektionszugriff, Dashboards, Fortschrittsanzeige und automatisierten Tests.",
            ],
        )
    )

    story.append(PageBreak())

    story.extend(section("Ausgewählte Projekte - Fortsetzung"))
    story.append(
        project(
            "Cryptoverse",
            "Frontend",
            "Kryptowährungs-Dashboard für globale Marktdaten, Ranglisten, Preisverläufe, Börsen und Nachrichten.",
            "React, Redux Toolkit, REST-APIs, Chart.js, Ant Design",
            "https://github.com/BenRoSang/cryptoverse",
            [
                "Integration externer APIs und zentrale Verwaltung des Anwendungszustands mit Redux Toolkit.",
                "Darstellung aktueller Marktdaten in durchsuchbaren Listen, Detailansichten und Diagrammen.",
            ],
        )
    )
    story.append(
        project(
            "Car Rental Service",
            "In Entwicklung",
            "Responsive Anwendung zur Fahrzeugsuche und -buchung mit Authentifizierung und CMS-verwalteten Fahrzeugdaten.",
            "Next.js, TypeScript, Tailwind CSS, Clerk, GraphQL, Hygraph",
            "https://github.com/BenRoSang/Car-Rental-Service",
            [
                "Entwicklung von Fahrzeugkatalog, Suche, Auswahl des Mietzeitraums und responsiven Layouts.",
                "Integration von Clerk für die Authentifizierung und Hygraph als GraphQL-basiertes CMS.",
            ],
        )
    )

    story.extend(section("Ausbildung"))
    story.append(role_header("Bachelor of Engineering (Elektronik)", "Kalay Technological University", "12/2011 - 08/2018", "Myanmar"))
    story.append(
        Paragraph(
            "Ingenieurwissenschaftliches Studium mit Schwerpunkt auf analytischem Denken, strukturierter Problemlösung und technischen Systemen.",
            styles["CVBody"],
        )
    )

    story.extend(section("Zertifikate & Weiterbildungen"))
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

    story.extend(section("Sprachkenntnisse"))
    language_rows = [
        [Paragraph("<b>Birmanisch</b><br/><font color='#526177'>Muttersprache</font>", styles["CVBodyDark"]),
         Paragraph("<b>Englisch</b><br/><font color='#526177'>Verhandlungssicher</font>", styles["CVBodyDark"]),
         Paragraph("<b>Deutsch</b><br/><font color='#526177'>B1 - Mittelstufe</font>", styles["CVBodyDark"])],
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

    story.extend(section("Weitere Angaben"))
    story.append(
        Paragraph(
            "Wohnhaft in Fürstenfeldbruck im Großraum München. Offen für Junior-Positionen im Frontend-, Full-Stack- und Webentwicklungsbereich sowie für Remote-, Hybrid- und Vor-Ort-Arbeit.",
            styles["CVBody"],
        )
    )

    document.build(story, onFirstPage=draw_header_de, onLaterPages=draw_header_de)
    PORTFOLIO_COPY.write_bytes(OUTPUT.read_bytes())


if __name__ == "__main__":
    build_cv_de()
    print(OUTPUT)
    print(PORTFOLIO_COPY)
