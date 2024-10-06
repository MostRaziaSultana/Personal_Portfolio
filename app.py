import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from wtforms import FileField,StringField,SelectField,SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
from flask import send_from_directory


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__)) 
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'site.db')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/images'
app.config['UPLOADED_CVS_DEST'] = 'static/uploads/cvs'

# Configure UploadSet

images = UploadSet('images', IMAGES)
cvs = UploadSet('cvs', ('pdf',))
configure_uploads(app, (images, cvs))


db = SQLAlchemy(app)

migrate = Migrate(app, db)

class ImageUploadForm(FlaskForm):
    description = StringField('Logo description', validators=[DataRequired()])
    image = FileField('Image', validators=[DataRequired()])
    favicon_image = FileField('Favicon Image', validators=[DataRequired()])



class Logo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True, default='not set')
    image = db.Column(db.String(200), nullable=True, default='not set')
    favicon_image = db.Column(db.String(200), nullable=True, default='not set')


class ImageModelView(ModelView):
    form = ImageUploadForm

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            filename = images.save(form.image.data)
            model.image = filename


        if form.favicon_image.data:
            favicon_filename = images.save(form.favicon_image.data)
            model.favicon_image = favicon_filename

class SideWidgetContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True, default='not set') 


class SocialMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=True, default='not set') 
    url = db.Column(db.String(200), nullable=True, default='not set') 
    icon_class = db.Column(db.String(50), nullable=True, default='not set')


class AboutMeUploadForm(FlaskForm):
    name = StringField('My Name', validators=[DataRequired()])
    designation = StringField('My designation', validators=[DataRequired()])
    image = FileField('My Image', validators=[DataRequired()])

class AboutMe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, default='not set')  
    designation =  db.Column(db.String(100), nullable=True, default='not set')
    image_url = db.Column(db.String(255), nullable=True, default='not set')

class AboutMeModelView(ModelView):
    form = AboutMeUploadForm

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            filename = images.save(form.image.data)
            model.image_url = filename

class AboutContentUploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    title_lastword = StringField('title_last_word', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    image = FileField('My Image', validators=[DataRequired()])
    cv_file = FileField('Upload CV (PDF only)', validators=[DataRequired()])

class AboutContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True, default='not set')
    title_lastword = db.Column(db.String(50), nullable=True, default='not set')
    description = db.Column(db.Text, nullable=True, default='not set')
    image_url = db.Column(db.String(255), nullable=True, default='not set')
    cv_file = db.Column(db.String(200), nullable=False, default='not set')

class AboutContentModelView(ModelView):
    form = AboutContentUploadForm

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            filename = images.save(form.image.data)
            model.image_url = filename

        if form.cv_file.data:
            cv_filename = cvs.save(form.cv_file.data)  # This will now work correctly
            model.cv_file = cv_filename

class CareerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False,default='Default description')


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=True, default='not set')
    company = db.Column(db.String(100), nullable=True, default='not set')
    duration = db.Column(db.String(50), nullable=True, default='not set')
    description = db.Column(db.Text, nullable=True, default='not set')


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=True, default='not set')
    skill_level = db.Column(db.Integer, nullable=True, default=None)

class ServiceHeader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False,default='Default description')


class ServiceUploadForm(FlaskForm):
    title = StringField('Service Title', validators=[DataRequired()])
    description = StringField('Service Description', validators=[DataRequired()])
    image = FileField('Service Logo', validators=[DataRequired()])


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default='Untitled Service')
    description = db.Column(db.Text, nullable=False,default='Default description')
    icon_url = db.Column(db.String(255), nullable=False, default='http://example.com/default-icon.png')

class ServiceModelView(ModelView):
    form = ServiceUploadForm
    def on_model_change(self, form, model, is_created):
        if form.image.data:
            filename = images.save(form.image.data)
            model.icon_url = filename

class ProjectHeader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False,default='Default description')

class ProjectUploadForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    link = StringField('Project Link', validators=[DataRequired()])
    image = FileField('Project Image', validators=[DataRequired()])

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False, default='http://example.com/default-project-image.png') 
    title = db.Column(db.String(100), nullable=False, default='Untitled Project')
    link = db.Column(db.String(255), nullable=False, default='http://example.com/default-link')

class ProjectModelView(ModelView):
    form = ProjectUploadForm

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            filename = images.save(form.image.data)
            model.image_url = filename


class CounterFact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon_class = db.Column(db.String(50), nullable=False, default='fa-icon-default')  
    value = db.Column(db.String(20), nullable=False, default='0')
    description = db.Column(db.String(100), nullable=False,default='Default description')


class BrandLogoUploadForm(FlaskForm):
    name = StringField('Brand Name', validators=[DataRequired()])
    image = FileField('Brand Logo', validators=[DataRequired()])

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='Unnamed Brand')
    image_url = db.Column(db.String(200), nullable=False, default='http://example.com/default-logo.png')

class BrandModelView(ModelView):
    form = BrandLogoUploadForm

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            filename = images.save(form.image.data)
            model.image_url = filename



class Copyright(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(4), nullable=False, default='2024')
    author = db.Column(db.String(100), nullable=False, default='Unknown Author') 


# -----------Contact Page------------

class ContactInfoUploadForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    phone1 = StringField('Phone 1', validators=[DataRequired()])
    phone2 = StringField('Phone 2')
    email1 = StringField('Email 1', validators=[DataRequired()])
    email2 = StringField('Email 2')
    image = FileField('Location Image', validators=[DataRequired()])

class ContactInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False, default='123 Main St, Anytown, USA') 
    phone1 = db.Column(db.String(15), nullable=False,default='000-000-0000')
    phone2 = db.Column(db.String(15), nullable=True,default=None)
    email1 = db.Column(db.String(100), nullable=False, default='example@example.com')
    email2 = db.Column(db.String(100), nullable=True, default=None)
    image = db.Column(db.String(200), nullable=True, default='not set')

class ContactInfoModelView(ModelView):
    form = ContactInfoUploadForm

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            filename = images.save(form.image.data)
            model.image = filename  # Save the filename to the model



class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='Anonymous')
    email = db.Column(db.String(100), nullable=False, default='no-reply@example.com')
    message = db.Column(db.Text, nullable=False, default='No message provided')

# -----------Portfolio Page------------
class PortfolioCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='Uncategorized')
    portfolio_items = db.relationship('PortfolioItem', backref='category', lazy=True)


class PortfolioItemUploadForm(FlaskForm):
    title = StringField('Portfolio title', validators=[DataRequired()])
    category = QuerySelectField('Category', query_factory=lambda: PortfolioCategory.query.all(), get_label='name', allow_blank=False)
    date = StringField('Date', validators=[DataRequired()])
    type = StringField('Project_type', validators=[DataRequired()])
    client = StringField('Client', validators=[DataRequired()])
    web_url = StringField('Web_url', validators=[DataRequired()])
    project_brief = StringField('Project brief', validators=[DataRequired()])
    image1 = FileField('Portfolio main Image', validators=[DataRequired()])
    image2 = FileField('Portfolio Detail Image1', validators=[DataRequired()])
    image3 = FileField('Portfolio Detail Image2', validators=[DataRequired()])
    image4 = FileField('Portfolio Detail Image3', validators=[DataRequired()])

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default='Untitled Portfolio Item')
    date = db.Column(db.String(50), nullable=False, default='2024-01-01')
    image1_url = db.Column(db.String(200), nullable=False, default='http://example.com/default-image.jpg')
    image2_url = db.Column(db.String(200), nullable=False, default='http://example.com/default-image.jpg')
    image3_url = db.Column(db.String(200), nullable=False, default='http://example.com/default-image.jpg')
    image4_url = db.Column(db.String(200), nullable=False, default='http://example.com/default-image.jpg')
    category_id = db.Column(db.Integer, db.ForeignKey('portfolio_category.id'), nullable=False,default=None)
    type = db.Column(db.String(100), nullable=False, default='Web Development')
    client = db.Column(db.String(100), nullable=False, default='Unknown')
    web_url = db.Column(db.String(200), nullable=False, default='http://example.com')
    project_brief = db.Column(db.Text, nullable=False, default='Default description')


class PortfolioItemModelView(ModelView):
    form = PortfolioItemUploadForm

    def create_form(self, obj=None):
        form = super(PortfolioItemModelView, self).create_form(obj)
        form.category.choices = [(c.id, c.name) for c in PortfolioCategory.query.all()]
        return form

    def edit_form(self, obj=None):
        form = super(PortfolioItemModelView, self).edit_form(obj)
        form.category.choices = [(c.id, c.name) for c in PortfolioCategory.query.all()]
        return form

    def on_model_change(self, form, model, is_created):
        # Check for each image field and save it if present
        if form.image1.data:
            filename1 = images.save(form.image1.data)
            model.image1_url = filename1
        if form.image2.data:
            filename2 = images.save(form.image2.data)
            model.image2_url = filename2
        if form.image3.data:
            filename3 = images.save(form.image3.data)
            model.image3_url = filename3
        if form.image4.data:
            filename4 = images.save(form.image4.data)
            model.image4_url = filename4




def create_tables():
    """Create database tables and add initial data if empty."""
    db.create_all()

    # Seed Logo data
    if Logo.query.count() == 0:
        logo = Logo(image_url="assets/img/logo/logo.png")
        db.session.add(logo)
        db.session.commit()

    # Seed SideWidgetContent data
    if SideWidgetContent.query.count() == 0:
        side_content = SideWidgetContent(
            content="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sint ratione reprehenderit, error qui enim sit ex provident iure, dolor, nulla eaque delectus, repudiandae commodi."
        )
        db.session.add(side_content)
        db.session.commit()

    # Seed SocialMedia data
    if SocialMedia.query.count() == 0:
        social_links = [
            SocialMedia(platform="Facebook", url="https://facebook.com", icon_class="fab fa-facebook-f"),
            SocialMedia(platform="Twitter", url="https://twitter.com", icon_class="fab fa-twitter"),
            SocialMedia(platform="LinkedIn", url="https://linkedin.com", icon_class="fab fa-linkedin-in"),
            SocialMedia(platform="Instagram", url="https://instagram.com", icon_class="fab fa-instagram"),
        ]
        db.session.add_all(social_links)
        db.session.commit()


    if AboutMe.query.count() == 0:
        about_me = AboutMe(name="Razia Sultana Shoily", designation="Frontend Designer | Developer | Sophisticated Engineer", image_url="assets/img/author/author1.png")
        db.session.add(about_me)

    db.session.commit()

    if AboutContent.query.count() == 0:
        about_content = AboutContent(
            title="Failure is the condiment That Gives",
            title_lastword="Success",
            description="Spend more time focusing on the important aspects of your business. Turn to McCartney HR LLC in Brooklyn, NY for HR solutions. As an advanced virtual HR company, we are offering online HR systems that can be customized depending on your business needs.",
            image_url="assets/img/author/author1.png"
        )
        db.session.add(about_content)
        db.session.commit()

    if CareerInfo.query.count() == 0:
        career_info = CareerInfo(
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sint ratione reprehenderit, error qui enim sit ex provident."
        )
        db.session.add(career_info)
        db.session.commit()

    if Experience.query.count() == 0:
        experiences = [
            Experience(job_title="UI Designer", company="Google Corporation", duration="2011 - 2014",
                       description="All you need to do your best work together in one package works seamlessly computer"),
            Experience(job_title="UI Designer", company="Apple Product Co.", duration="2011 - 2014",
                       description="All you need to do your best work together in one package works seamlessly computer"),
            Experience(job_title="Lead Designer", company="Musicsoft", duration="2011 - 2014",
                       description="All you need to do your best work together in one package works seamlessly computer"),
            Experience(job_title="UI Designer", company="Bruno Mars As.", duration="2011 - 2014",
                       description="All you need to do your best work together in one package works seamlessly computer"),
        ]
        db.session.add_all(experiences)
        db.session.commit()

    if Skill.query.count() == 0:
        skills = [
            Skill(skill_name="Branding Design", skill_level=90),
            Skill(skill_name="UI & UX Design", skill_level=85),
            Skill(skill_name="Web Design", skill_level=95),
            Skill(skill_name="Illustration", skill_level=80),
        ]
        db.session.add_all(skills)
        db.session.commit()

    if ServiceHeader.query.count() == 0:
        header = ServiceHeader(
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sint ratione reprehenderit, error qui enim sit ex provident."
        )
        db.session.add(header)
        db.session.commit()

    if Service.query.count() == 0:
        services = [
            Service(
                title="Design Principles",
                description="Need a project completed by an expert? Let’s go! Access a Human Resources Consultant to answer questions.",
                icon_url="assets/img/icon/service1.svg"
            ),
            Service(
                title="Unique Values",
                description="Need a project completed by an expert? Let’s go! Access a Human Resources Consultant to answer questions.",
                icon_url="assets/img/icon/service2.svg"
            ),
            Service(
                title="Style Components",
                description="Need a project completed by an expert? Let’s go! Access a Human Resources Consultant to answer questions.",
                icon_url="assets/img/icon/service3.svg"
            )
        ]
        db.session.bulk_save_objects(services)
        db.session.commit()

    if ProjectHeader.query.count() == 0:
        header = ProjectHeader(
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sint ratione reprehenderit."
        )
        db.session.add(header)
        db.session.commit()

    if Project.query.count() == 0:
        projects = [
            Project(image_url="assets/img/project/project1.png", title="Menu by Simon Jensen"),
            Project(image_url="assets/img/project/project2.png", title="Menu by Simon Jensen"),
            Project(image_url="assets/img/project/project3.png", title="Menu by Simon Jensen"),
            Project(image_url="assets/img/project/project4.png", title="Menu by Simon Jensen")
        ]
        db.session.bulk_save_objects(projects)
        db.session.commit()

    if CounterFact.query.count() == 0:

        sample_counter_facts = [
            CounterFact(
                icon_class='far fa-smile',
                value='100',
                description='Happy Clients'
            ),
            CounterFact(
                icon_class='far fa-clock',
                value='20',
                description='Support Team'
            ),
            CounterFact(
                icon_class='far fa-sliders-h',
                value='500',
                description='Sales Count'
            ),
            CounterFact(
                icon_class='far fa-trophy',
                value='10',
                description='Awards'
            )
        ]

        db.session.add_all(sample_counter_facts)
        db.session.commit()

    if Copyright.query.count() == 0:
        sample_copyright = Copyright(
            year='2019',
            author='QuomodoTheme',
        )
        db.session.add(sample_copyright)
        db.session.commit()

        contact = ContactInfo(
            address="9327 Prairie St. Grove City, OH 43123",
            phone1="+2546133254",
            phone2="+2545742516",
            email1="email@example.com",
            email2="info@yourdomain.com"
        )

        db.session.add(contact)
        db.session.commit()

    if PortfolioCategory.query.count() == 0:
        category_app_design = PortfolioCategory(name="App Design")
        category_design = PortfolioCategory(name="Design")
        category_agency = PortfolioCategory(name="Agency")
        category_branding = PortfolioCategory(name="Branding")

        db.session.add_all([category_app_design, category_design, category_agency, category_branding])
        db.session.commit()


    if PortfolioItem.query.count() == 0:
        portfolio1 = PortfolioItem(
            title="Architecture, Digital Art",
            date="29 November 2019",
            image_url="assets/img/portfolio-bg-1.jpg",
            category_id=1
        )
        portfolio2 = PortfolioItem(
            title="Another Architecture Project",
            date="15 August 2020",
            image_url="assets/img/portfolio-bg-2.jpg",
            category_id=2
        )
        db.session.add_all([portfolio1, portfolio_item2])
        db.session.commit()

    if Portfolio.query.count() == 0:
        portfolio1 = Portfolio(
            category="Web Development",
            date="02 October 2019",
            client="Oniblue",
            web_url="https://www.applanding.com",
            project_brief=("Far far away, behind the word mountains, "
                           "far from the countries Vokalia and Consonantia, "
                           "there live the blind texts..."),
        )
        portfolio2 = Portfolio(
            category="Graphic Design",
            date="29 November 2019",
            client="Design Company",
            web_url="https://www.designproject.com",
            project_brief=("A small river named Duden flows by their place..."),
        )

        db.session.add_all([portfolio_item1, portfolio_item2])
        db.session.commit()

    if Brand.query.count() == 0:
        default_brand = Brand(name="Default Brand", image_url="assets/img/logo/default_logo.png")
        db.session.add(default_brand)
        db.session.commit()


def initialize_app():
    """Initialize the application."""
    with app.app_context():
        create_tables()

@app.context_processor
def inject_globals():

    logo = Logo.query.first()
    side_content = SideWidgetContent.query.all()
    social_links = SocialMedia.query.all()
    about_me = AboutMe.query.first()
    about_content = AboutContent.query.first()
    career_info = CareerInfo.query.first()
    experiences = Experience.query.all()
    skills = Skill.query.all()
    service_header = ServiceHeader.query.first()
    services = Service.query.all()
    project_header = ProjectHeader.query.first()
    project_list = Project.query.all()
    counter_facts = CounterFact.query.all()
    copyright_info = Copyright.query.first()
    brands = Brand.query.all()


    return {
        'logo':logo,
        'side_content':side_content,
        'social_links':social_links,
        'about_me':about_me ,
        'about_content':about_content,
        'career_info':career_info,
        'experiences':experiences,
        'skills':skills,
        'service_header':service_header,
        'services':services,
        'project_header':project_header,
        'project_list':project_list,
        'counter_facts':counter_facts,
        'copyright':copyright_info,
        'brands':brands
    }



@app.route('/')
def home():
    logo = Logo.query.first()
    side_content = SideWidgetContent.query.all()
    social_links = SocialMedia.query.all()
    about_me = AboutMe.query.first()
    about_content = AboutContent.query.first()
    career_info = CareerInfo.query.first()
    experiences = Experience.query.all()
    skills = Skill.query.all()
    service_header = ServiceHeader.query.first()
    services = Service.query.all()
    project_header = ProjectHeader.query.first()
    project_list = Project.query.all()
    counter_facts = CounterFact.query.all()
    copyright_info = Copyright.query.first()
    brands = Brand.query.all()

    return render_template('index.html',
        logo=logo,
        side_content=side_content,
        social_links=social_links,
        about_me=about_me ,
        about_content=about_content,
        career_info=career_info,
        experiences=experiences,
        skills=skills,
        service_header=service_header,
        services=services,
        project_header=project_header,
        project_list=project_list,
        counter_facts=counter_facts,
        copyright=copyright_info,
        brands=brands
    )


# @app.route('/contactpage')
# def contact():
#     contact_info = ContactInfo.query.first()
#     return render_template('contact.html',contact=contact_info)


from flask import Flask, render_template, request, redirect, flash



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_info = ContactInfo.query.first()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        new_message = UserMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        flash('Your message has been sent successfully!', 'success')
        return redirect('/contact')

    return render_template('contact.html', contact=contact_info)

@app.route('/portfolio')
def portfolio():
    categories = PortfolioCategory.query.all()
    portfolio_items = PortfolioItem.query.all()
    return render_template('portfolio.html', categories=categories, portfolio_items=portfolio_items)


@app.route('/single-portfolio/<int:id>')
def single_portfolio(id):
    portfolio_item = PortfolioItem.query.get(id)
    return render_template('single-portfolio.html',portfolio_item=portfolio_item)


@app.route('/download_cv/<filename>')
def download_cv(filename):
    return send_from_directory(app.config['UPLOADED_CVS_DEST'], filename, as_attachment=True)



# Flask Admin setup
admin = Admin(app, name="Shoily's Panel", template_mode='bootstrap3')

admin.add_view(ImageModelView(Logo, db.session))
admin.add_view(ModelView(SideWidgetContent, db.session))
admin.add_view(ModelView(SocialMedia, db.session))
admin.add_view(AboutMeModelView(AboutMe, db.session))
admin.add_view(AboutContentModelView(AboutContent, db.session))
admin.add_view(ModelView(CareerInfo, db.session))
admin.add_view(ModelView(Experience, db.session))
admin.add_view(ModelView(Skill, db.session))
admin.add_view(ModelView(ServiceHeader, db.session))
admin.add_view(ServiceModelView(Service, db.session))
admin.add_view(ModelView(ProjectHeader, db.session))
admin.add_view(ProjectModelView(Project, db.session))
admin.add_view(ModelView(CounterFact, db.session))
admin.add_view(BrandModelView(Brand, db.session))
admin.add_view(ModelView(Copyright, db.session))
admin.add_view(ContactInfoModelView(ContactInfo, db.session))
admin.add_view(ModelView(UserMessage, db.session))
admin.add_view(ModelView(PortfolioCategory, db.session))
admin.add_view(PortfolioItemModelView(PortfolioItem, db.session))





if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
