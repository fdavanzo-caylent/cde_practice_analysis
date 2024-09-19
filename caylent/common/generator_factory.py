from caylent.salesforce.skills import generator as skills_heatmap_generator
from caylent.salesforce.weekly_engagements import generator as weekly_engagements_generator
from caylent.salesforce.cross_training_initiative import generator as cross_training_initiative_generator
from caylent.jira.work_in_progress import generator as wip_generator
from caylent.jira.time_in_status import generator as tis_generator
from caylent.jira.issue_throughput import generator as throughput_generator
from caylent.jira.cycle_time import generator as cycle_time_generator
from caylent.jira.cumulative_flow import generator as cumulative_flow_generator
from caylent.jira.issue_structure import generator as issue_structure_generator

GENERATORS = {
    'SKILLS_HEATMAP': skills_heatmap_generator,
    'WEEKLY_ENGAGEMENTS': weekly_engagements_generator,
    'WIP_ANALYSIS': wip_generator,
    'TIME_IN_STATUS_ANALYSIS': tis_generator,
    'ISSUE_THROUGHPUT': throughput_generator,
    'CYCLE_TIME': cycle_time_generator,
    'CUMULATIVE_FLOW': cumulative_flow_generator,
    'ISSUE_STRUCTURE': issue_structure_generator,
    'CROSS_TRAINING_INITIATIVE': cross_training_initiative_generator
}

def getGenerator(generator):
    return GENERATORS[generator]