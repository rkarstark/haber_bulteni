from readline import set_history_length
from rest_framework import serializers
from haberler.models import Makale


class MakaleSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayinlama_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only = True)
    guncellenme_tarihi = serializers.DateTimeField(read_only = True)
    

    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('baslik', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayinlama_tarihi = validated_data.get('yayinlama_tarihi', instance.yayinlama_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance