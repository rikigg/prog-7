from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from polls.models import Survey
from .serializers import ExportSurveySerializer
import csv
import json


class ExportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = ExportSurveySerializer

    @action(detail=True, methods=['get'])
    def csv(self, request, pk=None):
        survey = self.get_object()
        response = HttpResponse(content_type='text/csv')
        filename = f'survey_{survey.id}_{survey.title}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        writer.writerow(['Question', 'Choice', 'Votes'])
        
        for question in survey.question_set.all():
            for choice in question.choice_set.all():
                writer.writerow([
                    question.question_text,
                    choice.choice_text,
                    choice.votes
                ])
        
        return response

    @action(detail=True, methods=['get'])
    def json(self, request, pk=None):
        survey = self.get_object()
        serializer = self.get_serializer(survey)
        response = HttpResponse(
            json.dumps(serializer.data, indent=2),
            content_type='application/json'
        )
        filename = f'survey_{survey.id}_{survey.title}.json'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
