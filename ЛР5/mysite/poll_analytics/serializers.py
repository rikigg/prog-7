from rest_framework import serializers
from polls.models import Survey, Question, Choice, Answer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set')
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'pub_date', 'choices']

class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')
    total_votes = serializers.SerializerMethodField()
    
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'created_date', 'end_date', 
                 'is_active', 'questions', 'total_votes']
    
    def get_total_votes(self, obj):
        total = 0
        for question in obj.question_set.all():
            total += question.choice_set.aggregate(total=models.Sum('votes'))['total'] or 0
        return total 