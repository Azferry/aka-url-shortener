from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module

stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder

vanity_url_cr_measure = measure_module.MeasureInt("added vanity url",
                                            "number of added vanity urls",
                                            "vanity url")

vanity_url_cr_view = view_module.View("added vanity url ",
                                "number of added vanity urls",
                                ["application_type"],
                                vanity_url_cr_measure,
                                aggregation_module.CountAggregation()) 

short_url_cr_measure = measure_module.MeasureInt("added short url",
                                            "number of added short urls",
                                            "short url")
short_url_cr_view = view_module.View("added short url ",
                                "number of short urls created",
                                ["application_type"],
                                short_url_cr_measure,
                                aggregation_module.CountAggregation())

view_manager.register_view(short_url_cr_view)
view_manager.register_view(vanity_url_cr_view)
mmap = stats_recorder.new_measurement_map()
tmap = tag_map_module.TagMap()
tmap.insert("application_type", "flask")
tmap.insert("os_type", "linux")