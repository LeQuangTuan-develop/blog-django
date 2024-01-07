from django.db import models
from rest_framework import serializers, viewsets

# Model
class TestModel(models.Model):
    first_name = models.CharField(max_length=300, blank=False, null=True, default='')
    last_name = models.CharField(max_length=300, blank=False, null=True, default='')
    is_valid = models.SmallIntegerField(default=1)

    class Meta:
        '''Meta definition for Test.'''

        verbose_name = 'Test'
        verbose_name_plural = 'Test'

    def __str__(self):
        return self.first_name + ' - ' + self.last_name

# serializer
class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestModel
        fields = (
            'id',
            'first_name',
            'last_name',
            'is_valid'
        )

class CUTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestModel
        fields = (
            'first_name',
            'last_name',
        )

    def update(self, ins, validate_data):

        return super().update(ins, validate_data)



# view
class TestView(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    # serializer_class = TestSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TestSerializer

        return CUTestSerializer

class TestView(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    # serializer_class = TestSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TestSerializer

        return CUTestSerializer