# Generated by Django 4.1.3 on 2022-11-15 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='year_admission',
            field=models.PositiveIntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], default='2000', verbose_name='Год посткпления'),
        ),
        migrations.AlterField(
            model_name='group',
            name='number',
            field=models.CharField(default='00', max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to='profiles.group', verbose_name='Учебная группа'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(default=False, verbose_name='Является учителем'),
        ),
        migrations.AlterField(
            model_name='user',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Отчество'),
        ),
    ]
