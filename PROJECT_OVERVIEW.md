# News Portal 2025 Overview
Django 5.2 news platform with a public site, staff dashboard, and REST API. Uses DRF for APIs, Summernote for rich text, SQLite for storage, and Bootstrap-flavored templates.

## Quick Facts
- Frameworks: Django 5.2, DRF, Summernote, Bootstrap assets
- Data: SQLite (`db.sqlite3`); uploads under `media/`; static under `static/`
- Auth: Django auth with styled login/registration; staff flag gates dashboard

## App Roles (at a glance)
| App | Purpose | Highlights |
| --- | --- | --- |
| `newspaper` | Public site | Home/list/search/detail/contact/about; models for `Post`, `Category`, `Tag`, `Comment`, `Advertisement`, `Newsletter`, `Contact`, `UserProfile`, `OurTeam`; global `navigation` context processor for top categories. |
| `dashboard` | Staff CMS | Post/tag/category CRUD, draft publishing, newsletter email blast, unsubscribe endpoint. |
| `accounts` | Auth UI | Login/logout/registration views with Bootstrap-friendly forms. |
| `api` | REST API | Routers for users/groups/posts/categories/tags/contacts/newsletters; post-by-category/tag, drafts, publish, comments, and registration endpoints. |
| `NEWS` | Project config | Settings, URL routing, static/media/template setup. |

## Notable Behaviors
- Public pages show only active posts with `published_at`; detail increments `views_count` and surfaces category-related posts.
- Comments require authentication; success/error use Django messages.
- Newsletter subscribe via AJAX at `/newsletter/`; unsubscribe at `/dashboard/newsletter/unsubscribe/`.
- Dashboard actions are staff-only; new posts auto-assign the current user as author.
- API paginates (page size 10); anonymous reads for posts/categories/tags, admin-only writes unless noted.

## Key URLs (quick reference)
| Area | Routes | Notes |
| --- | --- | --- |
| Public | `/`, `/post-list/`, `/post-by-category/<id>/`, `/post-by-tag/<id>/`, `/post-detail/<pk>/`, `/search/?query=...`, `/contact/`, `/about/` | Active, published posts only; detail bumps `views_count`. |
| Auth | `/accounts/login/`, `/accounts/logout/`, `/accounts/register/` | Django auth with Bootstrap-styled forms. |
| Dashboard (staff) | `/dashboard/`, `/dashboard/post-create/`, `/dashboard/post-update/<pk>/`, `/dashboard/post-delete/<pk>/`, `/dashboard/draft-publish/<pk>/`, `/dashboard/tags/`, `/dashboard/categories/` | Staff-only CMS; draft publish also sends newsletter. |
| API root | `/api/v1/` | DRF browsable API; pagination size 10. |
| API extras | `/api/v1/post-by-category/<id>/`, `/api/v1/post-by-tag/<id>/`, `/api/v1/draft-list/`, `/api/v1/post-publish/`, `/api/v1/post/<post_id>/comments/`, `/api/v1/register/` | Public reads for posts/categories/tags; writes admin-only unless noted; comments POST requires auth. |

## Run It Locally
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # dashboard/API writes
python manage.py runserver
```
- Ensure `media/` is writable for uploads (post images, ads, team photos). Static files serve from `static/` during development.

## Files of Interest
- Settings/URLs: `NEWS/settings.py`, `NEWS/urls.py`
- Core site: `newspaper/models.py`, `newspaper/views.py`, `newspaper/urls.py`, `newspaper/nav.py`
- Dashboard: `dashboard/forms.py`, `dashboard/views.py`, `dashboard/urls.py`
- API: `api/serializers.py`, `api/views.py`, `api/urls.py`, `api/permissions.py`
- Auth: `accounts/forms.py`, `accounts/views.py`, `accounts/urls.py`
- Templates: `templates/` (public site, dashboard, registration)
