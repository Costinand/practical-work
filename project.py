import os
import csv

class PriceMachine():

    def __init__(self):
        self.data = []
'''загрузка прайс листов'''
    def load_prices(self, folder_path):
        key_mapping = {     # словарь тегов характеристик
            'название': ['название', 'продукт', 'товар', 'наименование'],
            'цена': ['цена', 'розница'],
            'вес': ['фасовка', 'масса', 'вес']
        }

        for file in os.listdir(folder_path):
            if "price" in file:  # проверка названия файла
                with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file, delimiter=',')  # прочтение файла
                    for row in csv_reader: # перебор строки документа
                        data = {'файл': file}
                        for key, possible_keys in key_mapping.items(): #  проверка содержимого строки
                            for possible_key in possible_keys:
                                if possible_key in row:
                                    data[key] = row[possible_key]
                                    break
                        self.data.append(data) # заполнение нового прайс-листа на основе представленных
                        
     '''поиск продукта по названию'''
    def search_product(self, search_query):
        results = [product for product in self.data if search_query.lower() in product.get('название', '').lower()]
        sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
        return sorted_results
    '''представление нового прайс-листа ввиде html документа'''
    def export_to_html(self, output_file_path=r'C:\\Users\\radag\\Work_20\\Practice\\output.html'):
        if self.data:
            sorted_data = sorted(self.data, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write('''
                <!DOCTYPE html>
                <html lang='ru'>
                <head>
                    <meta charset='UTF-8'>
                    <title>Позиции продуктов</title>
                </head>
                <body>
                    <table>
                        <tr>
                            <th>№</th>
                            <th>Наименование</th>
                            <th>Цена</th>
                            <th>Вес</th>
                            <th>Файл</th>
                            <th>Цена за кг.</th>
                        </tr>
                ''')
                for id, row in enumerate(sorted_data, start=1):
                    item_name = row.get('название', '')
                    price_per_kg = float(row.get('цена', 0)) / float(row.get('вес', 1))
                    file.write(
                        f"<tr><td>{id}</td><td>{item_name}</td><td>{row.get('цена', '')}</td><td>{row.get('вес', '')}</td><td>{row.get('файл', '')}</td><td>__{price_per_kg:.1f}</td></tr>"
                    )
                file.write('''
                    </table>
                </body>
                </html>
                ''')
            print(f"HTML файл успешно создан: {output_file_path}")
        else:
            print("Нет данных для экспорта в HTML файл.")

price_machine = PriceMachine()
price_machine.load_prices(r'C:\\Users\\radag\\Work_20\\Practice\\')

'''Работа с прайс-листами'''
try:
    while True:
        search_query = input("Введите наименование товара для поиска (или 'exit' для выхода): ")

        if search_query.lower() == 'exit':
            price_machine.export_to_html()
            print("Работа завершена.")
            break

        results = price_machine.search_product(search_query)

        if results:
            sorted_results = sorted(results, key=lambda x: float(x.get('цена', 0)) / float(x.get('вес', 1)))
            print("№         Наименование  Цена  Вес      Файл      Цена за кг")
            for id, result in enumerate(sorted_results, 1):
                print("%1s" % id, "%20s" % result.get('название'),
                      "%5s" % result.get('цена'), "%3s" % result.get('вес'),
                      "%13s" % result.get('файл'), "%9s" % (float(result.get('цена', 0)) / float(result.get('вес', 1))))

        else:
            print("Нет результатов по вашему запросу.")
            print(f"Вы искали: {search_query}")


except Exception as e:
    print(f"Произошла ошибка: {e}")