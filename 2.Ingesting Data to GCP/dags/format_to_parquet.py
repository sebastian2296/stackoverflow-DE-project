import logging
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.csv as pv
import pandas as pd


table_schema_posts_questions = pa.schema(
    [
        pa.field('id', pa.int64()),
        pa.field('title',pa.string()),
        pa.field('body',pa.string()),
        pa.field('accepted_answer_id',pa.float64()),
        pa.field('answer_count',pa.int64()),
        pa.field('comment_count',pa.int64()),
        pa.field('community_owned_date',pa.float64()),
        pa.field('creation_date',pa.timestamp('s')),
        pa.field('favorite_count',pa.float64()),
        pa.field('last_activity_date',pa.timestamp('s')),
        pa.field('last_edit_date',pa.timestamp('s')),
        pa.field('last_editor_display_name',pa.string()),
        pa.field('last_editor_user_id',pa.float64()),
        pa.field('owner_display_name',pa.string()),
        pa.field('owner_user_id',pa.float64()),
        pa.field('parent_id', pa.float64()),
        pa.field('post_type_id',pa.int64()),
        pa.field('score', pa.int64()),
        pa.field('tags', pa.string()),
        pa.field('view_count',pa.int64()),
        pa.field('group_by_date',pa.string())
    ] 
)

column_names_posts_questions = ['id',
 'title',
 'body',
 'accepted_answer_id',
 'answer_count',
 'comment_count',
 'community_owned_date',
 'creation_date',
 'favorite_count',
 'last_activity_date',
 'last_edit_date',
 'last_editor_display_name',
 'last_editor_user_id',
 'owner_display_name',
 'owner_user_id',
 'parent_id',
 'post_type_id',
 'score',
 'tags',
 'view_count',
 'group_by_date']

table_schema_post_answers = pa.schema(
    [
        pa.field('id',pa.int64()),
        pa.field('title',pa.float64()),
        pa.field('body',pa.string()),
        pa.field('accepted_answer_id',pa.float64()),
        pa.field('answer_count',pa.float64()),
        pa.field('comment_count',pa.int64()),
        pa.field('community_owned_date',pa.timestamp('s')),
        pa.field('creation_date',pa.timestamp('s')),
        pa.field('favorite_count',pa.float64()),
        pa.field('last_activity_date',pa.timestamp('s')),
        pa.field('last_edit_date',pa.timestamp('s')),
        pa.field('last_editor_display_name',pa.string()),
        pa.field('last_editor_user_id',pa.float64()),
        pa.field('owner_display_name',pa.string()),
        pa.field('owner_user_id',pa.float64()),
        pa.field('parent_id',pa.int64()),
        pa.field('post_type_id',pa.int64()),
        pa.field('score',pa.int64()),
        pa.field('tags',pa.float64()),
        pa.field('view_count',pa.float64()),
        pa.field('group_by_date',pa.string())
    ]
)

table_schema_users = pa.schema(
    [    
        pa.field('id',pa.int64()),
        pa.field('display_name',pa.string()),
        pa.field('about_me',pa.string()),
        pa.field('age',pa.float64()),
        pa.field('creation_date',pa.timestamp('s')),
        pa.field('last_access_date',pa.timestamp('s')),
        pa.field('location',pa.string()),
        pa.field('reputation',pa.int64()),
        pa.field('up_votes',pa.int64()),
        pa.field('down_votes',pa.int64()),
        pa.field('views',pa.int64()),
        pa.field('profile_image_url',pa.string()),
        pa.field('website_url',pa.string()),
        pa.field('group_by_date',pa.string())
    ]
)

table_schema_badges = pa.schema(
    [
        pa.field('id',pa.int64()),
        pa.field('name',pa.string()),
        pa.field('date',pa.timestamp('s')),
        pa.field('user_id',pa.int64()),
        pa.field('class',pa.int64()),
        pa.field('tag_based',pa.string()),
        pa.field('group_by_date',pa.string())
    ]
)


def parquetize(src_file, path):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return

    table = pd.read_csv(src_file)
    table.to_parquet(path)
