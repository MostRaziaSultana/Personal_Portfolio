"""Auto-detected migration

Revision ID: 3de04f8218a1
Revises: 7b86b5f09eb9
Create Date: 2024-10-03 01:51:31.335798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3de04f8218a1'
down_revision = '7b86b5f09eb9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('about_content', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title_lastword', sa.String(length=50), nullable=True))
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    with op.batch_alter_table('about_me', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('designation',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)

    with op.batch_alter_table('experience', schema=None) as batch_op:
        batch_op.alter_column('job_title',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('company',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('duration',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               nullable=True)

    with op.batch_alter_table('logo', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)

    with op.batch_alter_table('side_widget_content', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.TEXT(),
               nullable=True)

    with op.batch_alter_table('skill', schema=None) as batch_op:
        batch_op.alter_column('skill_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('skill_level',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('social_media', schema=None) as batch_op:
        batch_op.alter_column('platform',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('url',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
        batch_op.alter_column('icon_class',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('social_media', schema=None) as batch_op:
        batch_op.alter_column('icon_class',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('url',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
        batch_op.alter_column('platform',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('skill', schema=None) as batch_op:
        batch_op.alter_column('skill_level',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('skill_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    with op.batch_alter_table('side_widget_content', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.TEXT(),
               nullable=False)

    with op.batch_alter_table('logo', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)

    with op.batch_alter_table('experience', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('duration',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('company',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('job_title',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    with op.batch_alter_table('about_me', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('designation',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    with op.batch_alter_table('about_content', schema=None) as batch_op:
        batch_op.alter_column('image_url',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('description',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.drop_column('title_lastword')

    # ### end Alembic commands ###