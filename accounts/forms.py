from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

CustomUser = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        # UserCreationFormを継承しmodel変数とfields変数を上書き．
        model = CustomUser  # model = get_user_model() は NG
        fields = ("username", "email")


# password1, password2というフィールドはUserCreationFormの方で設定されているため、
# fieldsの欄には、Userモデルの中にある、
# blankにはできない値であるusernameとemailをセットする。
