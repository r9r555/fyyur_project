from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('1', 'AL'),
            ('2', 'AK'),
            ('3', 'AZ'),
            ('4', 'AR'),
            ('5', 'CA'),
            ('6', 'CO'),
            ('7', 'CT'),
            ('8', 'DE'),
            ('9', 'DC'),
            ('10', 'FL'),
            ('11', 'GA'),
            ('12', 'HI'),
            ('13', 'ID'),
            ('14', 'IL'),
            ('15', 'IN'),
            ('16', 'IA'),
            ('17', 'KS'),
            ('18', 'KY'),
            ('19', 'LA'),
            ('20', 'ME'),
            ('21', 'MT'),
            ('22', 'NE'),
            ('23', 'NV'),
            ('24', 'NH'),
            ('25', 'NJ'),
            ('26', 'NM'),
            ('27', 'NY'),
            ('28', 'NC'),
            ('29', 'ND'),
            ('30', 'OH'),
            ('31', 'OK'),
            ('32', 'OR'),
            ('33', 'MD'),
            ('34', 'MA'),
            ('35', 'MI'),
            ('36', 'MN'),
            ('37', 'MS'),
            ('38', 'MO'),
            ('39', 'PA'),
            ('40', 'RI'),
            ('41', 'SC'),
            ('42', 'SD'),
            ('43', 'TN'),
            ('44', 'TX'),
            ('45', 'UT'),
            ('46', 'VT'),
            ('47', 'VA'),
            ('48', 'WA'),
            ('49', 'WV'),
            ('50', 'WI'),
            ('51', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    def validateGenre(form, field):
        genreDict={
            1:'Alternative' ,
            2: 'Blues' ,
            3: 'Classical' ,
            4: 'Country' ,
            5: 'Electronic' ,
            6: 'Folk' ,
            7: 'Funk' ,
            8: 'Hip-Hop' ,
            9: 'Heavy Metal' ,
            10:'Instrumental' ,
            11: 'Jazz' ,
            12: 'Musical Theatre' ,
            13: 'Pop' ,
            14: 'Punk' ,
            15: 'R&B' ,
            16: 'Reggae' ,
            17: 'Rock n Roll' ,
            18: 'Soul' ,
            19: 'Other' }
        genreList =  genreDict.items()   
        for item  in genreList:     
            if item[1] == field.data:
            
            else:
                
        raise ValidationError("Sorry, you have chosen a wrong choice")

        
    genres = SelectMultipleField(
        # TODO implement enum restriction

        'genres', validators=[DataRequired()],
        choices=(
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        )
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
