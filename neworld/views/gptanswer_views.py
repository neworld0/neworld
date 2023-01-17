from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import Gpt, GptAnswer
from ..forms import GptAnswerForm
from pyChatGPT import ChatGPT
from captcha_solver import CaptchaSolver


# Bulletin Board 답변등록
@login_required(login_url='common:login')
def gptanswer_create(request, gpt_id):
    gpt = get_object_or_404(Gpt, pk=gpt_id)

    # auth with session token
    # session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..rFCa5K4-KWpCaNZP.EupHg6i1rgjXIbXpLx3bv2N_Ak1jQXyKJmuKLuVamcQWG2y5-YWeRSGYKYjamK-kREFy_EjnAJatOCpwBzCZ-MSaCdrhCNow6pnRjhbhJVD2anaRT2GWqrfw5eLdACKJ69Jp3g_rcXWhdex6NqpThGxNdXKwsZytp3DOjK65fyaniio4PYuBlQx4XJi-4ER5iYIH1juIaT7bg3ocDbdnDbmQz5FLVkAoGN3ScxpTpzKr1UubQ4dI3vFjbVJSXR1k4QTzJqaIQtjt6iXgtfx5S6eVH1ms1uyhpvzrgEAhEX_1Q6D3Q3DDV9IBydZoEn1ovyIT799O5-G5EO2Phpbqwmc63UAIzK881FpNcpCmE6xX8nbS0ZljbbJUMj6DHtVRImcUWWFkQ6Q-IskDRVqpV7LJ3B9PtqPJYHXtq4uARn5hLeEbd9hGEuHI3EjPtx8wo3haqHoytjzxGgmXFum26pkAcSralKqKLz3U6kWOHpm1h6CZFt2NreOsnONSXGfxN67vb0Z6QiTWnXuKsDyvIqTasUNJ7srLACBW2M-udSM4FsFlUVnQA0nkvHpoksOijzEeCRGIps3D90DUvVSmLFDjH8JOa332Vu7Iwof3sbON51Qk-hO7K2kma74W6jCBsmBzveq0VwdJ-yOawmQXG2VL6bgJZkDXtWqaHZTqIxwTWTKJ9UTAZENX0dR3k6Xt9BKzIPw1njUM-BuUdOvGvmHv5xiPmkbQT09_kxeMPyxvjZCZQKa8jmyXTDsjhWPvXny8yNERYPkOMvciKcw0SRZSV_X1EAey1PUaPkeqXHj2G-U5yjNbpDlELCjNKy7ft2O8T-YWMem1Q37NJMMVsxO1coCZXf-k5bnPUrJrhmwXnYgJgrWTHljIFm1esaOdKhtxYZgfvyEAh1oPEU6BRw86Wh9GArl_gCJ_hvzUUs8-D1j86ZCmlngsQQhrQqtUBeuj0hZolD4uoyrqU5sRAopSLkCca0tBuTU8-CvRnf9h8Gfgkp_CO_5ahPfAK3qUGte9yvR4mSzosVppWKHbTfqJDhTWSTXuMpgI3QctNXHAn-zqyhFSL42vgyvhhPBh0DoxWdO-XGc_XAg9FuQqYWN4r-_IPK-2uIFkgb4pSc93h1xp6d4fRuCthfOPODWkHL59ELswHgPxUh2c3m0pO1NJf3gidi_KFrroNF3OSLcvOMhlCzuNF8_N5q_yp4BUVUFvKcYZZ8Qo2yooOrQhLYKKNjuq2ToC3Ex6f4LXc-GXrcm0LiNLNA13UzU9zuyg_B5mP4m3EGNbZYQjKEbihxkiTg3mo3MC7pkwbFIudNHY4rd_prkJpLgUZ9L0ZYn-Q4BeR9LOxd1dj3q2TAVsDiTMjpbrY6pqoLF6cyNI0uzoTQ_h4G48LHQanNcPbEp---rXBjmpmWT4YehOgFi9xotS3Td7R5qpETJRZe7gquSInNFmBbcjKpwUgOolSYl6JrPQcOT-1RQdndFNVQPt35_rjs3em2ofAt93hEHwsohe45sq-4MayrOjmdABOL3ZK4ygsaJio6yQTjfHXHTGSMmOE1hfe1AcFEJd3hf_ggYbPOBUGNgt6lqgQ2iV-piUzq0dYtjQ4msnSFoIUvXniBto_kPEPbDAmtdaWHIsK4dKLv1MevNILDv7BfUlkX-3vc9TVN7K1DIFz00f4Qt0wY43rL-ZM8XYS8GLdTCzXcflJDCDRbVKIR4sy1hjXSoI_axUpCcUP5c4my_66i3BiWKwaQfitoui8E119ZEuzLEdOhlaTs9UB2XjTWi6F5kD3earY0m5ryML7JgV2UWM1SIOn92K9LVkWYuG-IYshqkoUcJgsC5gDclhtOuLOeDWW1ecWWmyiCSvS8LlQI-MHdW6MBUwlfkI0Pu7ZPbbYYRuDfp6YOvl64GDKkE7nbzsckRIpp8-_tKUXYOOURTaH2dSh8gV40vl-TJiZnxC9i--oK8PVus5DxIgZgbo6WCn9QBPoUpZr8mbFGMiBpmDS1wA5CiokynxA_9N--I6UNedMZBr6cLG-_jkDxB7-6bMtiv8XfHdj_RhmnuTZgoz1rTx4bRu3Jey-TpfHxRkzE1-tXU5gtPHwYe8nQTPwcn4SZSqg3sDVrf3Yy_eO9kDj7-oFGs7J3UN-HwCvbJ6QxSaNW6-KM46FwcrO4TjIFgJV-ryY6JnnE-iQt34uNJqvBPvvCsvZI0A69I-RQGv4lZTA5MXzmT4c5drrn5bmIqXJDdabMix4CqHoHjnNaLQezKY.P_6HMGSwlSKLa4Tg8sIoLg'
    # api = ChatGPT(session_token)

    # auth with google login
    api = ChatGPT(auth_type='google', email='neworld0@gmail.com', password='2tjdudEgjs!')

    # auth with openai login (captcha solving using speech-to-text engine)
    # api = ChatGPT(auth_type='openai', email='neworld@me.com', password='2tjdudEgjs!')

    gpt_q = gpt.content
    gptsend = api.send_message(gpt_q)
    gptanswer = GptAnswer(
                    content=gptsend['message'],
                    create_date=timezone.now(),
                    gpt=gpt
                ).save()
    context = {'gptanswer': gptanswer}
    return render(request, 'neworld/gpt_detail.html', context)


# # Bulletin Board 답변 수정
# @login_required(login_url='common:login')
# def gptanswer_modify(request, gptanswer_id):
#     gptanswer = get_object_or_404(GptAnswer, pk=gptanswer_id)
#     if request.user != gptanswer.author:
#         messages.error(request, '수정권한이 없습니다')
#         return redirect('neworld:gpt_detail', gpt_id=gptanswer.gpt.id)
#     if request.method == "POST":
#         form = GptAnswerForm(request.POST, instance=gptanswer)
#         if form.is_valid():
#             gptanswer = form.save(commit=False)
#             gptanswer.modify_date = timezone.now()
#             gptanswer.save()
#             return redirect('{}#gptanswer_{}'.format(
#                 resolve_url('neworld:detail', gpt_id=gptanswer.gpt.id), gptanswer.id))
#     else:
#         form = GptAnswerForm(instance=gptanswer)
#     context = {'gptanswer': gptanswer, 'form': form}
#     return render(request, 'neworld/gptanswer_form.html', context)
#
#
# # Bulletin Board 답변 삭제
# @login_required(login_url='common:login')
# def gptanswer_delete(request, gptanswer_id):
#     gptanswer = get_object_or_404(GptAnswer, pk=gptanswer_id)
#     if request.user != gptanswer.author:
#         messages.error(request, '삭제권한이 없습니다')
#     else:
#         gptanswer.delete()
#     return redirect('neworld:gpt_detail', gpt_id=gptanswer.gpt.id)

