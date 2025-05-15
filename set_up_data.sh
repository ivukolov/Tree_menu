case "$OSTYPE" in
    msys*)    python=python ;;
    cygwin*)  python=python ;;
    *)        python=python3 ;;
esac

$python manage.py migrate
$python manage.py test
$python manage.py flush --no-input
$python manage.py createsuperuser
echo "from menu.models import MenuItem; \
    main = MenuItem.objects.create(name='Menu', menu_name='main_menu', named_url='home'); \
    about = MenuItem.objects.create(name='About', menu_name='main_menu', named_url='about', parent=main); \
    contacts = MenuItem.objects.create(name='Contacts', menu_name='main_menu', named_url='contacts', parent=about); \
    trades = MenuItem.objects.create(name='Trades', menu_name='main_menu', named_url='trades',  parent=main);" | $python manage.py shell
echo "Setup done."