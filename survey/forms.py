from django.forms import ModelForm, Select, ChoiceField, ValidationError
from .models import Survey, Questionnaire


SURVEY_STORE = (
    ("002", "Survey of Research and Development Carried Out in the UK",),
    ("007", "Low Carbon and Renewable Energy Economy Survey",),
    ("009", "Monthly Business Survey",),
    ("014", "Annual PRODcom Survey PRODucts of the European COMmunity",),
    ("017", "Quarterly Stocks Survey",),
    ("019", "Quarterly Acquisitions and Disposals of Capital Assets Survey (QCAS) 019 - Quarterly Survey of Capital Expenditure",),
    ("022", "Quarterly Profits Inquiry",),
    ("023", "Monthly Business Survey - Retail Sales Index",),
    ("024", "Quarterly Fuels Inquiry",),
    ("057", "Quarterly International Trade in Services (QITIS)",),
    ("058", "Annual International Trade in Services (AITIS)",),
    ("061", "Services Provider Price Indices",),
    ("062", "Annual Inward Foreign Direct Investment Survey",),
    ("063", "Annual Outward Foreign Direct Investment Survey",),
    ("064", "Quarterly Inward Foreign Direct Investment Survey",),
)


class SurveyForm(ModelForm):

    survey_list = ChoiceField(choices=[(k, k + "-" + v) for k,v in SURVEY_STORE], label="Choose a Survey")

    class Meta:
        model = Survey
        exclude = ('title', 'survey_id')
        widgets = {
            'survey_list': Select(),
        }

    def clean_survey_list(self):
        survey_id = self.cleaned_data['survey_list']
        if Survey.objects.filter(survey_id=survey_id).exists():
            raise ValidationError("Survey has already been added")
        return survey_id

    def save(self):
        data = self.cleaned_data
        survey_id = data['survey_list']
        title = [item for item in SURVEY_STORE if item[0] == survey_id]
        survey = super(SurveyForm, self).save(commit=False)
        survey.title = title[0][1]
        survey.survey_id = survey_id
        survey.save()
        return survey
