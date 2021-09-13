from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Meditation, Comment, Research


# Bulletin Board 질문댓글 등록
@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question_c = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question_c
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'neworld/comment_form.html', context)


# Bulletin Board 질문댓글 수정
@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('neworld:detail', question_id=comment.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'neworld/comment_form.html', context)


# Bulletin Board 질문댓글 삭제
@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('neworld:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('neworld:detail', question_id=comment.question.id)


# Bulletin Board 답변댓글 등록
@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'neworld/comment_answer_form.html', context)


# Bulletin Board 답변댓글 수정
@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('neworld:detail', question_id=comment.answer.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'neworld/comment_form.html', context)


# Bulletin Board 답변댓글 삭제
@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('neworld:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('neworld:detail', question_id=comment.answer.question.id)


# Meditation 묵상댓글 등록
@login_required(login_url='common:login')
def comment_create_meditation(request, meditation_id):
    meditation = get_object_or_404(Meditation, pk=meditation_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.meditation = meditation
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:daily_scripture', scripture_id=comment.meditation.scripture.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'neworld/comment_meditation_form.html', context)


# Meditation 묵상댓글 수정
@login_required(login_url='common:login')
def comment_modify_meditation(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('neworld:daily_scripture', scripture_id=comment.meditation.scripture.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:daily_scripture', scripture_id=comment.meditation.scripture.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'neworld/comment_meditation_form.html', context)


# Meditation 묵상댓글 삭제
@login_required(login_url='common:login')
def comment_delete_meditation(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('neworld:daily_scripture', scripture_id=comment.meditation.scripture.id)
    else:
        comment.delete()
    return redirect('neworld:daily_scripture', scripture_id=comment.meditation.scripture.id)



# Research 조사내용 댓글 등록
@login_required(login_url='common:login')
def comment_create_research(request, research_id):
    research = get_object_or_404(Research, pk=research_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.research = research
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:weeklybible_detail', weeklybible_id=comment.research.weeklybible.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'neworld/comment_research_form.html', context)


# Research 조사내용 댓글 수정
@login_required(login_url='common:login')
def comment_modify_research(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('neworld:weeklybible_detail', weeklybible_id=comment.research.weeklybible.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:weeklybible_detail', weeklybible_id=comment.research.weeklybible.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'neworld/comment_research_form.html', context)


# Research 조사내용 댓글 삭제
@login_required(login_url='common:login')
def comment_delete_research(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('neworld:weeklybible_detail', weeklybible_id=comment.research.weeklybible.id)
    else:
        comment.delete()
    return redirect('neworld:weeklybible_detail', weeklybible_id=comment.research.weeklybible.id)
