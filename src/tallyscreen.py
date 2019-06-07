from machine import Pin, SPI
import max7219
import urequests
import utime

class TallyScreen():

    # uri = 'https://devvoh.com/tally-2018-test/export-latest-mutation'
    # uri = 'https://devvoh.com/tally-2018/export-latest-mutation'

    def __init__(self, spi_num=2, sck_pin=Pin(18), mosi_pin=Pin(23), cs_pin=Pin(5), screen_count=6 ):
        self.spi_num=spi_num
        self.sck_pin=sck_pin
        self.mosi_pin=mosi_pin
        self.cs_pin=cs_pin
        self.screen_count=screen_count

        self.spi = SPI(self.spi_num, sck=self.sck_pin, mosi=self.mosi_pin)
        self.display = max7219.Matrix8x8(self.spi, self.cs_pin, self.screen_count)

        self.uri = 'https://devvoh.com/tally-2018/export-latest-mutation'
        self.response = None
        self.created_at_timestamp = 0
        self.network_delay_ms = 200

        self.scroll_delay_ms = 125


#    def scroll_msg()

    def msg(self,msg):
        if (len (msg) > self.screen_count):
            msg += ' ' * self.screen_count
            for i in range(len(msg)-self.screen_count+1):
                self.display.fill(0)
                self.display.text(msg[i:i+self.screen_count], 0, 0, 1)
                self.display.show()
                utime.sleep_ms(self.scroll_delay_ms)
        else:
            self.display.fill(0)
            self.display.text(msg, 0, 0, 1)
            self.display.show()

    # confusing naming...
    def fetch(self):
        self.response = urequests.get(self.uri)
        return int(self.response.json()['metadata']['created_at_timestamp'])


    def is_updated(self):
        rmca = self.created_at_timestamp
        nwca = self.fetch()
        if nwca > rmca:
            self.created_at_timestamp = nwca
            return True
        else:
            return False


    def spinNumber(self, number):
        for i in range(number):
            self.msg(str(i))


    def displayBasicTally(self):
        parsed = self.response.json()
        message = '...' + parsed['player']['name'] + ' added ' + parsed['mutation']['amount'] + ' to his ' + parsed['tally']['name'] + ' for a total of ' + str(parsed['metadata']['tally_amount_total']) + '!'
        self.msg(message)


    def displayTally(self):
        parsed = self.response.json()
        message = '...' + parsed['player']['name'] + ' added ' + parsed['mutation']['amount'] + ' to his ' + parsed['tally']['name'] + ' for a total of '
        #+ str(parsed['metadata']['tally_amount_total']) + '!'
        self.msg(message)
        self.spinNumber(parsed['metadata']['tally_amount_total'])
        for i in range(5):
            self.msg(str(parsed['metadata']['tally_amount_total']))
            utime.sleep_ms(200)
            self.msg('')
            utime.sleep_ms(200)

######################

    def loop(self):
        """
        TODO: This blocks. Update to async polling?
        """
        while True:
            if self.is_updated() == True:
#                self.displayBasicTally()
                self.displayTally()
            utime.sleep_ms(self.network_delay_ms)

######################

    def fetchAndDisplay(self):
        """
        Just fetches and displays tally. Doesn't update tally displayTally
        """
        response = urequests.get(self.uri)
        parsed = response.json()
        message = parsed['player']['name'] + ' added ' + parsed['mutation']['amount'] + ' to his ' + parsed['tally']['name'] + ' for a total of ' + str(parsed['metadata']['tally_amount_total']) + '!'
        self.msg(message)
