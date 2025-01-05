from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from polls.models import Survey
from .serializers import SurveySerializer
import csv
import json
from django.utils import timezone


class SurveyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SurveySerializer

    def get_queryset(self):
        queryset = Survey.objects.all()
        
        # Фильтрация по датам
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(created_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_date__lte=date_to)

        # Сортировка
        sort_by = self.request.query_params.get('sort_by')
        if sort_by == 'date':
            queryset = queryset.order_by('-created_date')
        elif sort_by == 'votes':
            # Добавляем аннотацию для подсчета общего количества голосов
            queryset = queryset.annotate(
                total_votes=Count('question__choice__votes')
            ).order_by('-total_votes')

        return queryset

    @action(detail=True, methods=['get'])
    def export_csv(self, request, pk=None):
        survey = self.get_object()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{survey.title}_results.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Question', 'Choice', 'Votes'])
        
        for question in survey.question_set.all():
            for choice in question.choice_set.all():
                writer.writerow([question.question_text, choice.choice_text, choice.votes])
        
        return response

    @action(detail=True, methods=['get'])
    def export_json(self, request, pk=None):
        survey = self.get_object()
        serializer = self.get_serializer(survey)
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{survey.title}_results.json"'
        json.dump(serializer.data, response, indent=2)
        return response
