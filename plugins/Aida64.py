import json

import python_aida64

class Aida64:
    def __init__(self, core):
        self.core = core
        self.updater = {
            "timer": 5
        }
        self.discovery()

    def get_aida64_data(self):
        aida64_data = python_aida64.getData()
        if not aida64_data:
            self.core.log.error("Aida64数据读取失败")
            return None
        return aida64_data

    def discovery(self):
        category_counters = {
            'temp': 0,
            'pwr': 0,
            'fan': 0,
            'sys': 0,
            'volt': 0
        }

        info_lines = []
        aida64_data = self.get_aida64_data()
        if aida64_data:
            for category, items in aida64_data.items():
                if category not in category_counters:
                    continue

                for item in items:
                    name = item["label"]
                    entity_id = f"Aida64_{item["id"]}"

                    # 发送MQTT发现信息并记录结果
                    discovery_msg = self.core.mqtt.send_mqtt_discovery(
                        device_class=category,
                        num=category_counters[category],
                        name=name,
                        entity_id=entity_id,
                        is_aida64=True
                    )
                    info_lines.append(discovery_msg)
                    category_counters[category] += 1

            total_entities = sum(category_counters.values())
            self.core.log.debug(f"发送Aida64实体 Discovery MQTT信息,共{total_entities}个实体")

    def update_state(self):
        aida64_data = python_aida64.getData()
        if aida64_data:
            data = json.dumps(aida64_data)
            self.core.mqtt.update_state_data(data, "Aida64", "sensor")



