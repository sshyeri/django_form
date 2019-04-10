from django import forms
from .models import Board, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# class BoardForm(forms.Form):
#     title = forms.CharField(label='제목', widget=forms.TextInput(attrs={
#                                                     'placeholder': 'THE TITLE!',
#                                          }))
#     content = forms.CharField(label='내용', 
#                               error_messages={'required':'제발 내용을 입력해주세요!'},
#                               widget=forms.Textarea(attrs={
#                                                     'class': 'Content-input',
#                                                     'rows' : 5,
#                                                     'cols':50,
#                                                     'placeholder': 'Fill the Content!'
#                                          }))

#모델 안에 써도 되지만 나누는게 관례   
class BoardForm(forms.ModelForm):
    # Model의 정보를 작성하는 곳
    class Meta:
        model = Board
        # models.py에 지정해놓은 필드를 사용한다.
        fields = ['title', 'content', ]
        widgets = {'title' : forms.TextInput(attrs={
                                                    'placeholder':' 제목을 입력하세요.',
                                                    'class': 'title',}),
                  'content': forms.Textarea(attrs={
                                                    'placeholder': '내용을 입력하세요',
                                                    'class': 'content',
                                                    'rows':5,
                                                    'cols':50,})}
            
        error_messages = {'title': {
                                        'required': '제발 입력해주세요.'
                                    },
                          'content': {
                                        'required' : '내용 입력해주세요.'
                                     },
                        }
    #crispy forms 문서에 들어가면 있어요
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', '작성!'))
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]
       