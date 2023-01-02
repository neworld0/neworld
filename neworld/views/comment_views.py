from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Answer, Meditation, Comment, Research, Customer, Activity, Gpt, GptAnswer


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
    return render(request, 'neworld/comment_answer_form.html', context)


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


# 고객정보 댓글 등록
@login_required(login_url='common:login')
def comment_create_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.customer = customer
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:customer_detail', customer_id=comment.customer.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'neworld/comment_customer_form.html', context)


# 고객정보 댓글 수정
@login_required(login_url='common:login')
def comment_modify_customer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('neworld:customer_detail', customer_id=comment.customer.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:customer_detail', customer_id=comment.customer.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'neworld/comment_customer_form.html', context)


# 고객정보 댓글 삭제
@login_required(login_url='common:login')
def comment_delete_customer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('neworld:customer_detail', customer_id=comment.customer.id)
    else:
        comment.delete()
    return redirect('neworld:customer_detail', customer_id=comment.customer.id)



# 고객정보 활동 댓글 등록
@login_required(login_url='common:login')
def comment_create_activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.activity = activity
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:customer_detail', customer_id=comment.activity.customer.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'neworld/comment_activity_form.html', context)


# 고객정보 활동 댓글 수정
@login_required(login_url='common:login')
def comment_modify_activity(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('neworld:customer_detail', customer_id=comment.customer.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:customer_detail', customer_id=comment.activity.customer.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'neworld/comment_activity_form.html', context)


# 고객정보 활동 댓글 삭제
@login_required(login_url='common:login')
def comment_delete_activity(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('neworld:customer_detail', customer_id=comment.activity.customer.id)
    else:
        comment.delete()
    return redirect('neworld:customer_detail', customer_id=comment.activity.customer.id)



# Gpt 질문댓글 등록
@login_required(login_url='common:login')
def comment_create_gpt(request, gpt_id):
    gpt_c = get_object_or_404(Gpt, pk=gpt_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.gpt = gpt_c
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:gpt_detail', gpt_id=comment.gpt.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'neworld/comment_gpt_form.html', context)


# Gpt 질문댓글 수정
@login_required(login_url='common:login')
def comment_modify_gpt(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('neworld:gpt_detail', gpt_id=comment.gpt.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:gpt_detail', gpt_id=comment.gpt.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'neworld/comment_gpt_form.html', context)


# Gpt 질문댓글 삭제
@login_required(login_url='common:login')
def comment_delete_gpt(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('neworld:gpt_detail', gpt_id=comment.gpt.id)
    else:
        comment.delete()
    return redirect('neworld:gpt_detail', gpt_id=comment.gpt.id)


# Gpt 답변 댓글 등록
@login_required(login_url='common:login')
def comment_create_gptanswer(request, gptanswer_id):
    gptanswer = get_object_or_404(GptAnswer, pk=gptanswer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.gptanswer = gptanswer
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:gpt_detail', gpt_id=comment.gptanswer.gpt.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'neworld/comment_gptanswer_form.html', context)


# Gpt 답변 댓글 수정
@login_required(login_url='common:login')
def comment_modify_gptanswer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('neworld:gpt_detail', gpt_id=comment.gptanswer.gpt.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('neworld:gpt_detail', gpt_id=comment.gptanswer.gpt.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'neworld/comment_gptanswer_form.html', context)


# Gpt 답변댓글 삭제
@login_required(login_url='common:login')
def comment_delete_gptanswer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('neworld:gpt_detail', gpt_id=comment.gptanswer.gpt.id)
    else:
        comment.delete()
    return redirect('neworld:gpt_detail', gpt_id=comment.gptanswer.gpt.id)