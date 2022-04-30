from dataclasses import field
import imp
from pyexpat import model
from readline import set_history_length
from statistics import mode
from rest_framework import serializers
from haberler.models import Makale, Gazeteci
from datetime import datetime
from datetime import date
from django.utils.timesince import timesince


class MakaleSerializer(serializers.ModelSerializer):
    
    time_since_pub = serializers.SerializerMethodField()
    
    class Meta:
        model = Makale
        fields = '__all__'
        read_only_fiels = ['id', 'yaratilma_tarihi', 'guncellenme_tarihi']
    
    def get_time_since_pub(self, object):
        now = datetime.now()
        pub_date = object.yayinlama_tarihi
        if object.aktif == True:
            timedelta = timesince(pub_date, now)
            return timedelta
        else:
            return 'Aktif Degil!'
    
    def validate_yayinlama_tarihi(self, tarihdegeri):
        today = date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError('Tarih degeri ileri bi tarih olamaz')
        return tarihdegeri
        
class GazeteciSerializer(serializers.ModelSerializer):
    
    # makaleler = MakaleSerializer(many=True, read_only=True)

    makaleler = serializers.HyperlinkedRelatedField(
       many = True,
       read_only = True,
        view_name='makale-islem',
    )

    class Meta:
        model = Gazeteci
        field = '__all__'



































## STANDART SERIALIZER
class MakaleDefaultSerializer(serializers.Serializer):
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

    def validate(self, data):
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError(
                'Baslik ve aciklama alanlari ayni olamaz.'
            )
        return data

    def validate_baslik (self, value):
        if len(value) < 20:
            raise serializers.ValidationError(f'Minimum 20 karakter girebilirsiniz. Siz {len(value)} karakter girdiniz.')
        return value
