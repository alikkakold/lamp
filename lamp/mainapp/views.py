from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from mainapp.models import Board, Teammate, Column, Task


def main(request):
    if request.user.is_authenticated == True:
        return redirect(reverse('main:boards', kwargs={'user': request.user.username}))
    else:
        return render(request, 'mainapp/main.html')


@login_required(login_url='/auth/login/')
def boards(request, user):
    if request.method == 'POST':
        name = request.POST['name']
        type = request.POST['type']

        user_ = User.objects.get(username=user)

        Board.objects.create(name=name, type=type,
                             author=user_, token=hash(name + user_.username))

        return redirect(reverse("main:main"))
    else:
        u = User.objects.get(username=user)
        if u == request.user:
            board = Board.objects.filter(author=u)
            teammate_boards = Teammate.objects.filter(user=request.user)

            return render(request, 'mainapp/boards.html', {'boards': board,
                                                           'teammate_boards': teammate_boards,
                                                           'user': u,
                                                           'board_types': Board.CATEGORIES})
        else:
            # TODO: create a 404 error
            raise Exception('Permission denied')


@login_required(login_url="auth/login/")
def invite(request, board):
    board_ = get_object_or_404(Board, token=board)

    if not len(Teammate.objects.filter(board=board_, user=request.user)):
        Teammate.objects.create(board=board_, user=request.user)

    return redirect(reverse('main:boards', kwargs={'user': request.user}))


def board(request, user, board):
    board_ = get_object_or_404(Board, author__username=user, token=board)

    data = []

    for column in Column.objects.filter(board=board_):
        c = {}
        c['id'] = column.id
        c['name'] = column.name
        c['tasks'] = Task.objects.filter(column=column)
        data.append(c)


    return render(request, 'mainapp/board.html', {'board': board_,
                                                  'data': data})
