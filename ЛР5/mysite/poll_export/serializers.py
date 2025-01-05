from rest_framework import serializers
from django.db.models import Sum
from polls.models import Survey, Question, Choice


class ExportChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choice_text', 'votes']


class ExportQuestionSerializer(serializers.ModelSerializer):
    choices = ExportChoiceSerializer(many=True, source='choice_set')
    
    class Meta:
        model = Question
        fields = ['question_text', 'choices']


class ExportSurveySerializer(serializers.ModelSerializer):
    questions = ExportQuestionSerializer(many=True, source='question_set')
    total_votes = serializers.SerializerMethodField()
    
    class Meta:
        model = Survey
        fields = ['title', 'description', 'created_date', 'end_date', 
                 'questions', 'total_votes']
    
    def get_total_votes(self, obj):
        return obj.question_set.aggregate(
            total=Sum('choice__votes')
        )['total'] or 0 