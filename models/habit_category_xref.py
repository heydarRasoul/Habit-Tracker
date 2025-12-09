from db import db

habit_category_xref = db.Table(
    "HabitCategoryXref",
    db.Model.metadata,
    db.Column("habit_id", db.ForeignKey("Habits.habit_id", ondelete="CASCADE"), primary_key=True),
    db.Column("category_id", db.ForeignKey("HabitCategories.category_id", ondelete="CASCADE"), primary_key=True)
)