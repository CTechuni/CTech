from sqlalchemy.orm import Session
from app.modules.users.models import User
from app.modules.courses.models import Course
from app.modules.communities.models import Community
from app.modules.events.models import Event
from app.modules.mentoring_sessions.models import MentoringSession

def get_admin_metrics(db: Session):
    return {
        "total_users": db.query(User).count(),
        "total_courses": db.query(Course).count(),
        "total_communities": db.query(Community).count(),
        "total_events": db.query(Event).count(),
        "active_sessions": db.query(MentoringSession).filter(MentoringSession.is_available == False).count()
    }
