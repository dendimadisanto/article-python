from rest_framework import serializers

from .models import Data_mahasiswa
from .models import Artikel


class Data_mahasiswaSerializer(serializers.ModelSerializer):
  # nama = serializers.CharField(max_length=1000, required=True)

  # def create(self, validated_data):
  #   # Once the request data has been validated, we can create a Data_mahasiswa item instance in the database
  #   return Data_mahasiswa.objects.create(
  #     nama=validated_data.get('nama')
  #   )

  # def update(self, instance, validated_data):
  #    # Once the request data has been validated, we can update the Data_mahasiswa item instance in the database
  #   instance.nama = validated_data.get('nama', instance.nama)
  #   instance.save()
  #   return instance

  class Meta:
    model = Data_mahasiswa
    fields = '__all__'


class ArtikelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Artikel
    fields = '__all__'
