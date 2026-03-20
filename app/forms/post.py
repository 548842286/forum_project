from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('标题', validators=[
        DataRequired(message='标题不能为空'),
        Length(min=5, max=128, message='标题长度需在5-128个字符之间')
    ])
    content = TextAreaField('内容', validators=[
        DataRequired(message='内容不能为空'),
        Length(min=10, message='内容至少10个字符')
    ])
    board_id = SelectField('板块', coerce=int, validators=[DataRequired(message='请选择板块')])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    content = TextAreaField('评论', validators=[
        DataRequired(message='评论内容不能为空'),
        Length(min=1, max=1000, message='评论长度需在1-1000个字符之间')
    ])
    submit = SubmitField('发表评论')


class BoardForm(FlaskForm):
    name = StringField('板块名称', validators=[
        DataRequired(message='板块名称不能为空'),
        Length(min=2, max=64, message='板块名称长度需在2-64个字符之间')
    ])
    description = StringField('板块描述', validators=[
        Length(max=256, message='板块描述最多256个字符')
    ])
    submit = SubmitField('创建板块')
