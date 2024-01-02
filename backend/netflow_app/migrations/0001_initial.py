# Generated by Django 4.2.7 on 2024-01-02 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BaseNode',
            fields=[
                ('node_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DemandNode',
            fields=[
                ('basenode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='netflow_app.basenode')),
                ('demand_amount', models.FloatField(default=0)),
            ],
            bases=('netflow_app.basenode',),
        ),
        migrations.CreateModel(
            name='StorageNode',
            fields=[
                ('basenode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='netflow_app.basenode')),
                ('capacity', models.FloatField(default=0)),
                ('initial_amount', models.FloatField(default=0)),
            ],
            bases=('netflow_app.basenode',),
        ),
        migrations.CreateModel(
            name='SupplyNode',
            fields=[
                ('basenode_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='netflow_app.basenode')),
                ('supply_amount', models.FloatField(default=0)),
            ],
            bases=('netflow_app.basenode',),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_cost', models.FloatField()),
                ('arc_flows', models.JSONField(null=True)),
                ('arcs', models.ManyToManyField(related_name='solutions', to='netflow_app.arc')),
            ],
        ),
        migrations.AddField(
            model_name='arc',
            name='end_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_arcs', to='netflow_app.basenode'),
        ),
        migrations.AddField(
            model_name='arc',
            name='start_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_arcs', to='netflow_app.basenode'),
        ),
    ]
