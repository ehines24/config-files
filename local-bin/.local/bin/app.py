import nws
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # type: ignore
class Weather(Gtk.Window):
    def __init__(self, box_x = 62, box_y = 76):
        super().__init__(title="Next 48 Hours")
        scrolled_window=Gtk.ScrolledWindow()
        self.label = Gtk.Label()
        self.box_x = 62 
        self.box_y = 76
        self.label.set_markup(f"<span font=\"24\" font-family=\"Cascadia Code\"><b>Next 48 Hours:\n</b>{self.next_48_hours()}</span>")
        self.size = Gtk.Window.set_default_size(self, 900, 500)
        scrolled_window.add(self.label)
        scrolled_window.show()
        self.add(scrolled_window)
    def next_48_hours(self):
        forecasts = nws.get_hourly_forecasts(self.box_x, self.box_y)
        date = nws.get_date_of_forecast(self.box_x, self.box_y, 0)
        output = date + "\n"
        is_first_iteration = True
        for elem in forecasts[:48]: 
            output += elem + "\n"
            if(':' in elem):
                if(int(elem.split(':')[0]) == 0 and not is_first_iteration):
                    day = int(date[-2:])
                    day += 1
                    date = date[:-2] + str(day)
                    output += date + "\n"
                is_first_iteration = False
        print(output)
        return output
win = Weather()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
