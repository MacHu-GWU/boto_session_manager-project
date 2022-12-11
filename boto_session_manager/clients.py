# -*- coding: utf-8 -*-

import typing as T

from .services import AwsServiceEnum

if T.TYPE_CHECKING:
    from .manager import BotoSesManager


class ClientMixin:
    @property
    def accessanalyzer_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AccessAnalyzer)

    @property
    def account_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Account)

    @property
    def acm_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ACM)

    @property
    def acm_pca_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ACMPCA)

    @property
    def alexaforbusiness_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AlexaForBusiness)

    @property
    def amp_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.PrometheusService)

    @property
    def amplify_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Amplify)

    @property
    def amplifybackend_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AmplifyBackend)

    @property
    def amplifyuibuilder_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AmplifyUIBuilder)

    @property
    def apigateway_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.APIGateway)

    @property
    def apigatewaymanagementapi_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ApiGatewayManagementApi)

    @property
    def apigatewayv2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ApiGatewayV2)

    @property
    def appconfig_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AppConfig)

    @property
    def appconfigdata_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AppConfigData)

    @property
    def appflow_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Appflow)

    @property
    def appintegrations_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AppIntegrationsService)

    @property
    def application_autoscaling_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ApplicationAutoScaling)

    @property
    def application_insights_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ApplicationInsights)

    @property
    def applicationcostprofiler_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ApplicationCostProfiler)

    @property
    def appmesh_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AppMesh)

    @property
    def apprunner_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AppRunner)

    @property
    def appstream_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AppStream)

    @property
    def appsync_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AppSync)

    @property
    def arc_zonal_shift_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ARCZonalShift)

    @property
    def athena_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Athena)

    @property
    def auditmanager_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AuditManager)

    @property
    def autoscaling_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AutoScaling)

    @property
    def autoscaling_plans_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AutoScalingPlans)

    @property
    def backup_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Backup)

    @property
    def backup_gateway_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.BackupGateway)

    @property
    def backupstorage_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.BackupStorage)

    @property
    def batch_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Batch)

    @property
    def billingconductor_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.BillingConductor)

    @property
    def braket_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Braket)

    @property
    def budgets_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Budgets)

    @property
    def ce_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CostExplorer)

    @property
    def chime_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Chime)

    @property
    def chime_sdk_identity_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ChimeSDKIdentity)

    @property
    def chime_sdk_media_pipelines_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ChimeSDKMediaPipelines)

    @property
    def chime_sdk_meetings_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ChimeSDKMeetings)

    @property
    def chime_sdk_messaging_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ChimeSDKMessaging)

    @property
    def chime_sdk_voice_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ChimeSDKVoice)

    @property
    def cloud9_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Cloud9)

    @property
    def cloudcontrol_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudControlApi)

    @property
    def clouddirectory_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudDirectory)

    @property
    def cloudformation_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudFormation)

    @property
    def cloudfront_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudFront)

    @property
    def cloudhsm_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudHSM)

    @property
    def cloudhsmv2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudHSMV2)

    @property
    def cloudsearch_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudSearch)

    @property
    def cloudsearchdomain_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudSearchDomain)

    @property
    def cloudtrail_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudTrail)

    @property
    def cloudwatch_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudWatch)

    @property
    def codeartifact_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeArtifact)

    @property
    def codebuild_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeBuild)

    @property
    def codecatalyst_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeCatalyst)

    @property
    def codecommit_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeCommit)

    @property
    def codedeploy_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeDeploy)

    @property
    def codeguru_reviewer_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeGuruReviewer)

    @property
    def codeguruprofiler_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeGuruProfiler)

    @property
    def codepipeline_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodePipeline)

    @property
    def codestar_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeStar)

    @property
    def codestar_connections_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeStarconnections)

    @property
    def codestar_notifications_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CodeStarNotifications)

    @property
    def cognito_identity_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CognitoIdentity)

    @property
    def cognito_idp_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CognitoIdentityProvider)

    @property
    def cognito_sync_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CognitoSync)

    @property
    def comprehend_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Comprehend)

    @property
    def comprehendmedical_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ComprehendMedical)

    @property
    def compute_optimizer_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ComputeOptimizer)

    @property
    def config_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ConfigService)

    @property
    def connect_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Connect)

    @property
    def connect_contact_lens_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ConnectContactLens)

    @property
    def connectcampaigns_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ConnectCampaignService)

    @property
    def connectcases_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ConnectCases)

    @property
    def connectparticipant_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ConnectParticipant)

    @property
    def controltower_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ControlTower)

    @property
    def cur_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CostandUsageReportService)

    @property
    def customer_profiles_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CustomerProfiles)

    @property
    def databrew_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.GlueDataBrew)

    @property
    def dataexchange_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DataExchange)

    @property
    def datapipeline_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DataPipeline)

    @property
    def datasync_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DataSync)

    @property
    def dax_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DAX)

    @property
    def detective_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Detective)

    @property
    def devicefarm_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DeviceFarm)

    @property
    def devops_guru_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DevOpsGuru)

    @property
    def directconnect_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DirectConnect)

    @property
    def discovery_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ApplicationDiscoveryService)

    @property
    def dlm_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DLM)

    @property
    def dms_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DatabaseMigrationService)

    @property
    def docdb_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DocDB)

    @property
    def docdb_elastic_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DocDBElastic)

    @property
    def drs_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.drs)

    @property
    def ds_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DirectoryService)

    @property
    def dynamodb_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DynamoDB)

    @property
    def dynamodbstreams_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.DynamoDBStreams)

    @property
    def ebs_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EBS)

    @property
    def ec2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EC2)

    @property
    def ec2_instance_connect_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EC2InstanceConnect)

    @property
    def ecr_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ECR)

    @property
    def ecr_public_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ECRPublic)

    @property
    def ecs_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ECS)

    @property
    def efs_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EFS)

    @property
    def eks_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EKS)

    @property
    def elastic_inference_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ElasticInference)

    @property
    def elasticache_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ElastiCache)

    @property
    def elasticbeanstalk_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ElasticBeanstalk)

    @property
    def elastictranscoder_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ElasticTranscoder)

    @property
    def elb_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ElasticLoadBalancing)

    @property
    def elbv2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ElasticLoadBalancingv2)

    @property
    def emr_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EMR)

    @property
    def emr_containers_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EMRContainers)

    @property
    def emr_serverless_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EMRServerless)

    @property
    def es_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ElasticsearchService)

    @property
    def events_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EventBridge)

    @property
    def evidently_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudWatchEvidently)

    @property
    def finspace_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.finspace)

    @property
    def finspace_data_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.FinSpaceData)

    @property
    def firehose_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Firehose)

    @property
    def fis_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.FIS)

    @property
    def fms_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.FMS)

    @property
    def forecast_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ForecastService)

    @property
    def forecastquery_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ForecastQueryService)

    @property
    def frauddetector_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.FraudDetector)

    @property
    def fsx_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.FSx)

    @property
    def gamelift_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.GameLift)

    @property
    def gamesparks_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.GameSparks)

    @property
    def glacier_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Glacier)

    @property
    def globalaccelerator_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.GlobalAccelerator)

    @property
    def glue_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Glue)

    @property
    def grafana_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ManagedGrafana)

    @property
    def greengrass_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Greengrass)

    @property
    def greengrassv2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.GreengrassV2)

    @property
    def groundstation_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.GroundStation)

    @property
    def guardduty_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.GuardDuty)

    @property
    def health_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Health)

    @property
    def healthlake_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.HealthLake)

    @property
    def honeycode_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Honeycode)

    @property
    def iam_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IAM)

    @property
    def identitystore_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IdentityStore)

    @property
    def imagebuilder_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.imagebuilder)

    @property
    def importexport_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ImportExport)

    @property
    def inspector_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Inspector)

    @property
    def inspector2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Inspector2)

    @property
    def iot_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoT)

    @property
    def iot_data_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTDataPlane)

    @property
    def iot_jobs_data_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTJobsDataPlane)

    @property
    def iot_roborunner_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTRoboRunner)

    @property
    def iot1click_devices_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoT1ClickDevicesService)

    @property
    def iot1click_projects_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoT1ClickProjects)

    @property
    def iotanalytics_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTAnalytics)

    @property
    def iotdeviceadvisor_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTDeviceAdvisor)

    @property
    def iotevents_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTEvents)

    @property
    def iotevents_data_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTEventsData)

    @property
    def iotfleethub_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTFleetHub)

    @property
    def iotfleetwise_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTFleetWise)

    @property
    def iotsecuretunneling_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTSecureTunneling)

    @property
    def iotsitewise_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTSiteWise)

    @property
    def iotthingsgraph_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTThingsGraph)

    @property
    def iottwinmaker_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTTwinMaker)

    @property
    def iotwireless_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IoTWireless)

    @property
    def ivs_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IVS)

    @property
    def ivschat_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ivschat)

    @property
    def kafka_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Kafka)

    @property
    def kafkaconnect_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.KafkaConnect)

    @property
    def kendra_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.kendra)

    @property
    def keyspaces_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Keyspaces)

    @property
    def kinesis_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Kinesis)

    @property
    def kinesis_video_archived_media_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.KinesisVideoArchivedMedia)

    @property
    def kinesis_video_media_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.KinesisVideoMedia)

    @property
    def kinesis_video_signaling_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.KinesisVideoSignalingChannels)

    @property
    def kinesisanalytics_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.KinesisAnalytics)

    @property
    def kinesisanalyticsv2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.KinesisAnalyticsV2)

    @property
    def kinesisvideo_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.KinesisVideo)

    @property
    def kms_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.KMS)

    @property
    def lakeformation_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LakeFormation)

    @property
    def lambda_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Lambda)

    @property
    def lex_models_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LexModelBuildingService)

    @property
    def lex_runtime_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LexRuntimeService)

    @property
    def lexv2_models_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LexModelsV2)

    @property
    def lexv2_runtime_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LexRuntimeV2)

    @property
    def license_manager_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LicenseManager)

    @property
    def license_manager_user_subscriptions_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LicenseManagerUserSubscriptions)

    @property
    def lightsail_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Lightsail)

    @property
    def location_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LocationService)

    @property
    def logs_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudWatchLogs)

    @property
    def lookoutequipment_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LookoutEquipment)

    @property
    def lookoutmetrics_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LookoutMetrics)

    @property
    def lookoutvision_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.LookoutforVision)

    @property
    def m2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MainframeModernization)

    @property
    def machinelearning_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MachineLearning)

    @property
    def macie_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Macie)

    @property
    def macie2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Macie2)

    @property
    def managedblockchain_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ManagedBlockchain)

    @property
    def marketplace_catalog_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MarketplaceCatalog)

    @property
    def marketplace_entitlement_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MarketplaceEntitlementService)

    @property
    def marketplacecommerceanalytics_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MarketplaceCommerceAnalytics)

    @property
    def mediaconnect_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MediaConnect)

    @property
    def mediaconvert_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MediaConvert)

    @property
    def medialive_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MediaLive)

    @property
    def mediapackage_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MediaPackage)

    @property
    def mediapackage_vod_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MediaPackageVod)

    @property
    def mediastore_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MediaStore)

    @property
    def mediastore_data_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MediaStoreData)

    @property
    def mediatailor_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MediaTailor)

    @property
    def memorydb_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MemoryDB)

    @property
    def meteringmarketplace_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MarketplaceMetering)

    @property
    def mgh_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MigrationHub)

    @property
    def mgn_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.mgn)

    @property
    def migration_hub_refactor_spaces_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MigrationHubRefactorSpaces)

    @property
    def migrationhub_config_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MigrationHubConfig)

    @property
    def migrationhuborchestrator_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MigrationHubOrchestrator)

    @property
    def migrationhubstrategy_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MigrationHubStrategyRecommendations)

    @property
    def mobile_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Mobile)

    @property
    def mq_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MQ)

    @property
    def mturk_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MTurk)

    @property
    def mwaa_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.MWAA)

    @property
    def neptune_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Neptune)

    @property
    def network_firewall_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.NetworkFirewall)

    @property
    def networkmanager_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.NetworkManager)

    @property
    def nimble_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.NimbleStudio)

    @property
    def oam_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudWatchObservabilityAccessManager)

    @property
    def omics_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Omics)

    @property
    def opensearch_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.OpenSearchService)

    @property
    def opensearchserverless_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.OpenSearchServiceServerless)

    @property
    def opsworks_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.OpsWorks)

    @property
    def opsworkscm_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.OpsWorksCM)

    @property
    def organizations_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Organizations)

    @property
    def outposts_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Outposts)

    @property
    def panorama_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Panorama)

    @property
    def personalize_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Personalize)

    @property
    def personalize_events_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.PersonalizeEvents)

    @property
    def personalize_runtime_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.PersonalizeRuntime)

    @property
    def pi_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.PI)

    @property
    def pinpoint_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Pinpoint)

    @property
    def pinpoint_email_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.PinpointEmail)

    @property
    def pinpoint_sms_voice_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.PinpointSMSVoice)

    @property
    def pinpoint_sms_voice_v2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.PinpointSMSVoiceV2)

    @property
    def pipes_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EventBridgePipes)

    @property
    def polly_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Polly)

    @property
    def pricing_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Pricing)

    @property
    def privatenetworks_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Private5G)

    @property
    def proton_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Proton)

    @property
    def qldb_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.QLDB)

    @property
    def qldb_session_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.QLDBSession)

    @property
    def quicksight_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.QuickSight)

    @property
    def ram_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.RAM)

    @property
    def rbin_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.RecycleBin)

    @property
    def rds_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.RDS)

    @property
    def rds_data_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.RDSDataService)

    @property
    def redshift_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Redshift)

    @property
    def redshift_data_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.RedshiftDataAPIService)

    @property
    def redshift_serverless_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.RedshiftServerless)

    @property
    def rekognition_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Rekognition)

    @property
    def resiliencehub_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ResilienceHub)

    @property
    def resource_explorer_2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ResourceExplorer)

    @property
    def resource_groups_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ResourceGroups)

    @property
    def resourcegroupstaggingapi_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ResourceGroupsTaggingAPI)

    @property
    def robomaker_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.RoboMaker)

    @property
    def rolesanywhere_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.IAMRolesAnywhere)

    @property
    def route53_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Route53)

    @property
    def route53_recovery_cluster_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Route53RecoveryCluster)

    @property
    def route53_recovery_control_config_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Route53RecoveryControlConfig)

    @property
    def route53_recovery_readiness_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Route53RecoveryReadiness)

    @property
    def route53domains_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Route53Domains)

    @property
    def route53resolver_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Route53Resolver)

    @property
    def rum_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.CloudWatchRUM)

    @property
    def s3_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.S3)

    @property
    def s3control_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.S3Control)

    @property
    def s3outposts_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.S3Outposts)

    @property
    def sagemaker_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SageMaker)

    @property
    def sagemaker_a2i_runtime_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AugmentedAIRuntime)

    @property
    def sagemaker_edge_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SagemakerEdgeManager)

    @property
    def sagemaker_featurestore_runtime_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SageMakerFeatureStoreRuntime)

    @property
    def sagemaker_geospatial_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SageMakergeospatialcapabilities)

    @property
    def sagemaker_runtime_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SageMakerRuntime)

    @property
    def savingsplans_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SavingsPlans)

    @property
    def scheduler_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.EventBridgeScheduler)

    @property
    def schemas_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Schemas)

    @property
    def sdb_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SimpleDB)

    @property
    def secretsmanager_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SecretsManager)

    @property
    def securityhub_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SecurityHub)

    @property
    def securitylake_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SecurityLake)

    @property
    def serverlessrepo_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ServerlessApplicationRepository)

    @property
    def service_quotas_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ServiceQuotas)

    @property
    def servicecatalog_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ServiceCatalog)

    @property
    def servicecatalog_appregistry_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.AppRegistry)

    @property
    def servicediscovery_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ServiceDiscovery)

    @property
    def ses_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SES)

    @property
    def sesv2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SESV2)

    @property
    def shield_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Shield)

    @property
    def signer_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.signer)

    @property
    def simspaceweaver_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SimSpaceWeaver)

    @property
    def sms_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SMS)

    @property
    def sms_voice_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.PinpointSMSVoice)

    @property
    def snow_device_management_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SnowDeviceManagement)

    @property
    def snowball_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Snowball)

    @property
    def sns_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SNS)

    @property
    def sqs_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SQS)

    @property
    def ssm_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SSM)

    @property
    def ssm_contacts_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SSMContacts)

    @property
    def ssm_incidents_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SSMIncidents)

    @property
    def ssm_sap_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SsmSap)

    @property
    def sso_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SSO)

    @property
    def sso_admin_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SSOAdmin)

    @property
    def sso_oidc_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SSOOIDC)

    @property
    def stepfunctions_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SFN)

    @property
    def storagegateway_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.StorageGateway)

    @property
    def sts_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.STS)

    @property
    def support_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Support)

    @property
    def support_app_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SupportApp)

    @property
    def swf_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.SWF)

    @property
    def synthetics_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Synthetics)

    @property
    def textract_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Textract)

    @property
    def timestream_query_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.TimestreamQuery)

    @property
    def timestream_write_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.TimestreamWrite)

    @property
    def transcribe_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.TranscribeService)

    @property
    def transfer_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Transfer)

    @property
    def translate_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.Translate)

    @property
    def voice_id_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.VoiceID)

    @property
    def waf_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WAF)

    @property
    def waf_regional_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WAFRegional)

    @property
    def wafv2_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WAFV2)

    @property
    def wellarchitected_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WellArchitected)

    @property
    def wisdom_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.ConnectWisdomService)

    @property
    def workdocs_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WorkDocs)

    @property
    def worklink_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WorkLink)

    @property
    def workmail_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WorkMail)

    @property
    def workmailmessageflow_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WorkMailMessageFlow)

    @property
    def workspaces_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WorkSpaces)

    @property
    def workspaces_web_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.WorkSpacesWeb)

    @property
    def xray_client(self: "BotoSesManager"):
        return self.get_client(AwsServiceEnum.XRay)
