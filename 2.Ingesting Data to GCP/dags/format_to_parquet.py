import logging
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.csv as pv


table_schema_posts_questions = pa.schema(
    [
    ('id', pa.int64()),
    ('title', pa.string()),
    ('body',  pa.string()),
    ('accepted_answer_id', pa.float64()),
    ('answer_count',pa.int64()),
    ('comment_count', pa.int64()),
    ('community_owned_date', pa.float64()),
    ('creation_date',  pa.timestamp('s')),
    ('favorite_count', pa.float64()),
    ('last_activity_date', pa.timestamp('s')),
    ('last_edit_date', pa.timestamp('s')),
    ('last_editor_display_name', pa.string()),
    ('last_editor_user_id',  pa.float64()),
    ('owner_display_name',  pa.string()),
    ('owner_user_id', pa.float64()),
    ('parent_id', pa.float64()),
    ('post_type_id', pa.int64()),
    ('score', pa.int64()),
    ('tags', pa.string()),
    ('view_count', pa.int64())
] )

table_schema_post_answers = pa.schema(
    [
    ('id',                          pa.int64()),
    ('title',                       pa.float64()),
    ('body',                        pa.string()),
    ('accepted_answer_id',          pa.float64()),
    ('answer_count',                pa.float64()),
    ('comment_count',               pa.int64()),
    ('community_owned_date',        pa.timestamp('s')),
    ('creation_date',               pa.timestamp('s')),
    ('favorite_count',              pa.float64()),
    ('last_activity_date',          pa.timestamp('s')),
    ('last_edit_date',              pa.timestamp('s')),
    ('last_editor_display_name',    pa.string()),
    ('last_editor_user_id',         pa.float64()),
    ('owner_display_name',          pa.string()),
    ('owner_user_id',               pa.float64()),
    ('parent_id',                   pa.int64()),
    ('post_type_id',                pa.int64()),
    ('score',                       pa.int64()),
    ('tags',                        pa.float64()),
    ('view_count',                  pa.float64())
    ]
)
table_schema_users = pa.schema(
[    
    ('id',                   pa.int64()),
    ('display_name',         pa.string()),
    ('about_me',             pa.string()),
    ('age',                  pa.float64()),
    ('creation_date',        pa.timestamp('s')),
    ('last_access_date',     pa.timestamp('s')),
    ('location',             pa.string()),
    ('reputation',           pa.int64()),
    ('up_votes',             pa.int64()),
    ('down_votes',           pa.int64()),
    ('views',                pa.int64()),
    ('profile_image_url',    pa.string()),
    ('website_url',          pa.string())
    ]
)

table_schema_badges = pa.schema(
[
    ('id',               pa.int64()),
    ('name',             pa.string()),
    ('date',             pa.timestamp('s')),
    ('user_id',          pa.int64()),
    ('class',            pa.int64()),
    ('tag_based',        pa.string()),
    ('group_by_date',    pa.string())
]
)


def parquetize(src_file, service, ti):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return

    table = pv.read_csv(src_file)
  
    table = table.cast(f'table_schema_{service}')
    
    parquet_table = pq.write_table(table, src_file.replace('.csv', '.parquet'))
    ti.xcom_push(key='parquet_file',value=parquet_table)