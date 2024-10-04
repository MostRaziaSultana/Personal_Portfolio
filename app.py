from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate

from flask_wtf import FlaskForm
from flask_uploads import UploadSet, configure_uploads, IMAGES
from wtforms import FileField
from wtforms.validators import DataRequired

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/images'

# Configure UploadSet
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class ImageUploadForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired()])


class Logo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=True, default='not set')


class ImageModelView(ModelView):
    form = ImageUploadForm

    def on_model_change(self, form, model, is_created):
        # Save the uploaded image and store its path in the database
        if form.image.data:
            filename = images.save(form.image.data)  # Save the image
            model.image_url = filename  # Save the path to the database


class SideWidgetContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True, default='not set') 


class SocialMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=True, default='not set') 
    url = db.Column(db.String(200), nullable=True, default='not set') 
    icon_class = db.Column(db.String(50), nullable=True, default='not set')  

class AboutMe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True, default='not set')  
    designation =  db.Column(db.String(100), nullable=True, default='not set')
    image_url = db.Column(db.String(255), nullable=True, default='not set')


class AboutContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True, default='not set')
    title_lastword = db.Column(db.String(50), nullable=True, default='not set')
    description = db.Column(db.Text, nullable=True, default='not set')
    image_url = db.Column(db.String(255), nullable=True, default='not set')

class CareerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)


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
    description = db.Column(db.Text, nullable=False)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon_url = db.Column(db.String(255), nullable=False)

class ProjectHeader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(255), nullable=False)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)

class TestimonialEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), nullable=False)
    author_location = db.Column(db.String(100), nullable=False)
    testimonial_text = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

class CounterFact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon_class = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)





class Copyright(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(4), nullable=False)
    author = db.Column(db.String(100), nullable=False)


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
            Project(image_url="assets/img/project/project1.png", title="Menu by Simon Jensen", link="portfolio.html"),
            Project(image_url="assets/img/project/project2.png", title="Menu by Simon Jensen", link="portfolio.html"),
            Project(image_url="assets/img/project/project3.png", title="Menu by Simon Jensen", link="portfolio.html"),
            Project(image_url="assets/img/project/project4.png", title="Menu by Simon Jensen", link="portfolio.html")
        ]
        db.session.bulk_save_objects(projects)
        db.session.commit()

    if Testimonial.query.count() == 0:
        testimonial = Testimonial(
            description="Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sint ratione reprehenderit"
        )
        db.session.add(testimonial)
        db.session.commit()

    if TestimonialEntry.query.count() == 0:
        sample_testimonials = [
            TestimonialEntry(
                author_name="Jack Metiyo Shina",
                author_location="NYC, USA",
                testimonial_text="Gilroy is a great and super-professional service provider, which brought new technologies, new methodology, and a fresh perspective to our project.",
                image_url="assets/img/author/testimonial1.jpg"
            ),
            # Add more testimonials as needed
        ]
        db.session.bulk_save_objects(sample_testimonials)
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


def initialize_app():
    """Initialize the application."""
    with app.app_context():
        create_tables()

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
    testimonial = Testimonial.query.first()
    testimonialentry = TestimonialEntry.query.all()
    counter_facts = CounterFact.query.all()
    copyright_info = Copyright.query.first()

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
        testimonial=testimonial,
        testimonialentry=testimonialentry,
        counter_facts=counter_facts,
        copyright=copyright_info
    )


@app.route('/contact')
def contact():
    return render_template('contact.html')

# Flask Admin setup
admin = Admin(app, name="Shoily's Panel", template_mode='bootstrap3')

admin.add_view(ImageModelView(Logo, db.session))
admin.add_view(ModelView(SideWidgetContent, db.session))
admin.add_view(ModelView(SocialMedia, db.session))
admin.add_view(ModelView(AboutMe, db.session))
admin.add_view(ModelView(AboutContent, db.session))
admin.add_view(ModelView(CareerInfo, db.session))
admin.add_view(ModelView(Experience, db.session))
admin.add_view(ModelView(Skill, db.session))
admin.add_view(ModelView(ServiceHeader, db.session))
admin.add_view(ModelView(Service, db.session))
admin.add_view(ModelView(ProjectHeader, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Testimonial, db.session))
admin.add_view(ModelView(TestimonialEntry, db.session))
admin.add_view(ModelView(CounterFact, db.session))
admin.add_view(ModelView(Copyright, db.session))



if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
