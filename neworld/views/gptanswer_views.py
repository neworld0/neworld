from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..models import Gpt, GptAnswer
from ..forms import GptAnswerForm
from pyChatGPT import ChatGPT


# Bulletin Board 답변등록
@login_required(login_url='common:login')
def gptanswer_create(request, gpt_id):
    gpt = get_object_or_404(Gpt, pk=gpt_id)
    session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..bWRmOuckGhyN7-IK.WRuMzg0-r4I8cWX0Na8Z3ZmkKCu-qp6asWlySftk0FphdBnGmDl81DG6lc64S4wjjEFAB1wgE1FhNVp1SsqiFQHkM-rciXij3riF2adrfcejQIwlhRYsWGX2T_MtM3GEGSHXa93EM1LGbyHtVDe0svyRRVv3BpRQhKaKAzpluG0pV6M_CFYFMCfR-iuOr6em6lbGBD0MLEJe4H_TFhkYUzsbIF6VQUf92uqQLc-0JtfPgSMr8i-xiPCrkpDEeRVfIn3828LpZuQib_7Y7-h-enJ3EKVGe3rFAYp1j6d6BnA0SuJkQ2_5jKuwVhy-5cATH5uhsiKxXCkl8c3iWNlmlTl3c-UTE4WZRcHAzEdaJt9LjGSC_va5mMR3J4nHnseuq3xyvxXRP0ULOCcH9jZtB8mQNrgUSfjcjxO6l0ChdHRDdvz7QmSZGgYCPepmM2sT_0H9zNHNKexKD_NEXAjDZmmsMvXyjcY7zK-Bnq6LaP7Qr6JudPfn7iVK07MlM8L39i5mqveCmhRqC56IfmDvID8L09Jl_Q8Ea0QjMxRqY8lYUrZhnwPNpMO3gNRDQwS0fA90uAMymFv1T1ort0ELRYvUUqjcKV1zNVwYEqmVnyIFFRORkwSv8ukY6Z6E-eHq9ZX0vvRBAR6dnt5--rIdIkvXj0_uvn7UmftMo2jEvBcPcqam3cXw92JOf-2Rmnp0sxgNN72Yx97YYvsfxtQV7tbenX4gHvYX_eYictXTk_LgOtM5ad8g7NjKclVXjO19v1ScRRqRjatfGbruvYMEjXK4HRUncsqzopez_4Fg9qAwwkmlDklaQkd65FXVu4NRj_2bBTZgsT-jpv8LiufTWnUNoUm59lwkAZJUeq_FvxNEjBw1yCZZN--RQ8EDCu71y_bZGAjeOQIRP7tMSCkrK_IyQkG-b0tbo1z2-ZjHjnSsGURvcLeBCYCNybTHFYkhRrpPdvL_oS24lnJhYl6sTlXPBLngT4NeOATvIjUlZfVhqS8cR6VkdHP3htaaEpr1wQnSPP24dyOIXWP10OGWG36WnDZ8w8ZFHGy5AuLbVLFDj3C__XjYnQKpd-mW7X_df_1Rx1Y151JaNVJXCKryQu1-uzUu5R1PWJdV76fO32x5JKAcoSIKV-yBQ_2rqMsfPcrdqnDX67WpuGQ5hQb4l2PXiJwCXNltnJkR6JkJI61VdDv1GqvvdZJP3Jyjp7BXW7a0nXc2oPNUxv9x_JlYq67ZH0isX4yz6dUqeB_ypQIBGdCRsUqnNxZukVvtZ8i_gVcmKQxsh7ePn9DVVWRQZCW121kr98vQeQGxl_JpjB6Qg-3y_EKEjRhbKrB_cJukwNKn2n1v4pl9EzPxqF8BA6PqqXwdbOdFOdX4ERVOvACMaFKsz4LyDDlpZSU9rx1YDmYX9BBzozweZHwssBLERkjdFrKDKw84tkCYMcdyc_V-vbeqkYHgpHy_aObT3qntIw8G4xxryRBUyjn6MPll9TMMkClR1_KE3YC0-AUfn1Q1PEiet3F1YrTj0vPWtNBfXVU9NLGLA7t7uQ-gVombFR766WUiUmUESCUXDx0fyjDo0C9csF41Yng50z21nCvwUT1mlcD3AUxJFhvdY2op4vmPY0PN4PIUnf9d2yd6QPE2uvAdSLu7D1KNXTq6rXm643YW0c0vgz4K6dV8aj0088CKrpEITToOoazOROMKtV8-tTTXRIm9292NMEzrzDA5ar1oR3fJ9hbGA3XOqsnegLr7Xb3hSAn9KPjuIlo4KLb5oKu6cLPDbSWjqE-yFRIHG0uggQTElRsO1ozevBT17X9UxYeKBPaIADk1V_qQp4msQC-QyiiozdVoIxkB32XVDFc3tl8oSWvPU8_Z5RtBKlvoANkaXVpcLceC8ZeZDeQoTjxK8cVnqt11WvYwQe2GrdmjoIXyoy-vHWKON2oq_601wLF7B6ey0_7Sjjhn2dvC-jtV_K3po-23RwdAzQ9hZUSbHIRRaOFLvVwX4zlBq4XEbORz1t3tY_O91J8pAhMVnPIKVAiTrpp9azUOHjnbgHpBzcgPSaw4C4hd0Hjj8OVsarwRE-0rvhZmXL3T2rncM-kR0RLaVINvzbxXyMLxMrFSvaMZAm33890Qm-UZaVgTe7YATMmyJCyW8Zs1SHXbnE-CLx22OsUeh-wC-6deYET2TevO43LC7752BIsDm9lGE2QTlRJRb33t-g7cH5qYMzb8t2z0STnOaWbLiMujm_zFPg6DGppLvi9a_hRKeFUZ.1lg-BjUxkboor6v5er97qw'  # `__Secure-next-auth.session-token` cookie from https://chat.openai.com/chat
    api = ChatGPT(session_token)  # auth with session token
    gpt_q = gpt.content
    gptsend = api.send_message(gpt_q)
    gptanswer = GptAnswer(
                    author=request.user,
                    content=gptsend['message'],
                    create_date=timezone.now(),
                    gpt=gpt
                ).save()
    context = {'gptanswer': gptanswer}
    return render(request, 'neworld/gpt_detail.html', context)


# Bulletin Board 답변 수정
@login_required(login_url='common:login')
def gptanswer_modify(request, gptanswer_id):
    gptanswer = get_object_or_404(GptAnswer, pk=gptanswer_id)
    if request.user != gptanswer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('neworld:gpt_detail', gpt_id=gptanswer.gpt.id)
    if request.method == "POST":
        form = GptAnswerForm(request.POST, instance=gptanswer)
        if form.is_valid():
            gptanswer = form.save(commit=False)
            gptanswer.modify_date = timezone.now()
            gptanswer.save()
            return redirect('{}#gptanswer_{}'.format(
                resolve_url('neworld:detail', gpt_id=gptanswer.gpt.id), gptanswer.id))
    else:
        form = GptAnswerForm(instance=gptanswer)
    context = {'gptanswer': gptanswer, 'form': form}
    return render(request, 'neworld/gptanswer_form.html', context)


# Bulletin Board 답변 삭제
@login_required(login_url='common:login')
def gptanswer_delete(request, gptanswer_id):
    gptanswer = get_object_or_404(GptAnswer, pk=gptanswer_id)
    if request.user != gptanswer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        gptanswer.delete()
    return redirect('neworld:gpt_detail', gpt_id=gptanswer.gpt.id)

