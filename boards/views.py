from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Board, Comment
from .forms import BoardForm, CommentForm

# Create your views here.
def index(request):
    boards = get_list_or_404(Board.objects.order_by('-pk'))
    context = {'boards':boards}
    return render(request, 'boards/index.html', context)

@login_required
def create(request):
    # POST 요청이면 FORM 데이터를 처리한다.
    if request.method == 'POST':
        #이 처리과정은 'binding'으로 불리는데, 폼의 유효성 체크를 할 수 있도록 해준다.
        form = BoardForm(request.POST)
        #form 유효성 체크
        if form.is_valid():
            # board 를 바로 저장하지 않고, 현재 user를 넣고 저장
            # 실제 DB에 반영 전까지의 단계를 진행하고, 그 중간에 user 정보를
            # reqeust.user에서 가져와서 그 후에 저장한다.
            board = form.save(commit=False) 
            board.user = request.user
            board.save()
            # 모델 폼은 검증이 필요 없어요. 이미 모델에서 검증.
            # title = form.cleaned_data.get('title')
            # content = form.cleaned_data.get('content')
            # #검증을 통과한 깨끗한 데이터를 form에서 가져와서 board를 만든다. 
            # board = Board.objects.create(title=title, content=content)
            return redirect('boards:detail', board.pk)
    #GET 요청(혹은 다른 메서드)이면 기본 폼을 생성한다.
    else:
        form = BoardForm()
    context = {'form':form }
    return render(request, 'boards/form.html', context)
        
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    comments = board.comment_set.all()
    form = CommentForm()
    context = { 'board' : board,
                'comments' : comments,
                'form' : form,
    }
    return render(request, 'boards/detail.html', context)
    
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:index')

@login_required        
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user:
        if request.method == 'POST':
            form = BoardForm(request.POST, instance=board)
            if form.is_valid():
                board = form.save()
                # board.title = form.cleaned_data.get('title')
                # board.content = form.cleaned_data.get('content')
                # board.save()
                return redirect('boards:detail', board.pk)
        #GET 요청이면(수정하기 버튼을 눌렀을 때)
        else:
            #BoardForm을 초기화(사용자 입력 값을 넣어준 상태로)
            #form = BoardForm(initial={'title':board.title, 'content':board.content})
            form = BoardForm(instance=board)
            # form = BoardForm(initial=board.__dict__)
        #1. POST:요청에서 검증에 실패하였을 때, 오류 메세지가 포함된 상태
        #2. GET : 요청에서 초기화된 상태
    else: 
        return redirect('boards:index')
    context={
        'form':form, 
        'board':board,
        
    }
    return render(request, 'boards/form.html', context)
        
@require_POST
@login_required
def comment_create(request, board_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.board_id = board_pk
        comment.user = request.user
        comment.save()
        return redirect('boards:detail', board_pk)

@require_POST
@login_required
def comment_delete(request, board_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('boards:detail', board_pk)

