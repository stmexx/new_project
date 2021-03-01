from wavy import render, Application
from models import TrainingSite
from logging_mod import Logger, debug

site = TrainingSite()
logger = Logger('main')


def main_view(request):
    logger.log('Список курсов')
    print(f'Список курсов - {site.courses}')
    return '200 OK', render('course_list.html', objects_list=site.courses)


@debug
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.append(course)
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        name = Application.decode_value(name)
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


def index(request):
    secret = request.get('secret_key', None)
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    return '200 OK', "About"


def contact_view(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Нам пришло сообщение от {email} с темой {title} и текстом {text}')
        return '200 OK', render('contact.html')
    else:
        return '200 OK', render('contact.html')


urlpatterns = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category,
    # '/copy-course/': copy_course,
    # '/category-list/': category_list,
    '/index/': index,
    '/contact/': contact_view,
    '/about/': about_view

}


def secret_controller(request):
    request['secret'] = 'secret'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)


# application = DebugApplication(urlpatterns, front_controllers)
# application = FakeApplication(urlpatterns, front_controllers)


@application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)


