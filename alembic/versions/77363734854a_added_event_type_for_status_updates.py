"""Added event type for status updates

Revision ID: 77363734854a
Revises: 6ca1d79395fe
Create Date: 2021-12-20 19:43:18.736072

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '77363734854a'
down_revision = '6ca1d79395fe'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TYPE event_type ADD VALUE \'STATUS_UPDATE\';')


def downgrade():
    raise Exception('Irreversible migration, new event_type added')
