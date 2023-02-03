from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

CustomUser = get_user_model()

# ユーザー作成時にはDjango側で UserCreationForm という便利なフォームを用意してくれているのでこれを用います


class SignupForm(UserCreationForm):
    class Meta:
        # UserCreationFormを継承しmodel変数とfields変数を上書き．
        model = CustomUser  # model = get_user_model() は NG
        fields = ("username", "email")
        # models.pyで作ったemailフィールドとAbstractUserに元から含まれるusernameを書く
        # password1, password2というフィールドはUserCreationFormの方で設定されているため、
        # fieldsの欄には、Userモデルの中にある、
        # blankにはできない値であるusernameとemailをセットする。


class LoginForm(AuthenticationForm):
    pass
