from db import db

user_challenge_xref = db.Table(
    "userChallengeXref",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("Users.user_id", ondelete="CASCADE"), primary_key=True),
    db.Column("category_id", db.ForeignKey("HabitChallenges.challenge_id", ondelete="CASCADE"), primary_key=True)
)