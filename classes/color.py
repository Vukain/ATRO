class BColors:
    # standardowe
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    VIOLET = '\033[35m'
    CYAN = '\033[36m'
    GREY = '\033[37m'
    FG = '\033[39m'
    DGREY = '\033[90m'
    # intensywne
    ISTAND = '\033[30m'
    IRED = '\033[91m'
    IGREEN = '\033[92m'
    IYELLOW = '\033[93m'
    IBLUE = '\033[94m'
    IVIOLET = '\033[95m'
    ICYAN = '\033[96m'
    IOPPO = '\033[97m'
    # tło
    BRED = '\033[41m'
    BGREEN = '\033[42m'
    BYELLOW = '\033[43m'
    BBLUE = '\033[44m'
    BVIOLET = '\033[45m'
    BCYAN = '\033[46m'
    BGREY = '\033[47m'
    BG = '\033[49m'
    BDGREY = '\033[100m'
    # tło intensywne
    BISTAND = '\033[40m'
    BIRED = '\033[101m'
    BIGREEN = '\033[102m'
    BIYELLOW = '\033[103m'
    BIBLUE = '\033[104m'
    BIVIOLET = '\033[105m'
    BICYAN = '\033[106m'
    BIOPPO = '\033[107m'
    # efekty
    BOLD = '\033[1m'
    ITAL = '\033[3m'
    UNDER = '\033[4m'
    SWAP = '\033[7m'
    ENDC = '\033[0m'

    def disable(self):
        self.GREY = ''
        self.RED = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.BLUE = ''
        self.VIOLET = ''
        self.CYAN = ''
        self.DGREY = ''
        self.ISTAND = ''
        self.IRED = ''
        self.IGREEN = ''
        self.IYELLOW = ''
        self.IBLUE = ''
        self.IVIOLET = ''
        self.ICYAN = ''
        self.IOPPO = ''
        self.BGREY = ''
        self.BRED = ''
        self.BGREEN = ''
        self.BYELLOW = ''
        self.BBLUE = ''
        self.BVIOLET = ''
        self.BCYAN = ''
        self.BDGREY = ''
        self.BISTAND = ''
        self.BIRED = ''
        self.BIGREEN = ''
        self.BIYELLOW = ''
        self.BIBLUE = ''
        self.BIVIOLET = ''
        self.BICYAN = ''
        self.BIOPPO = ''
        self.FG = ''
        self.BG = ''
        self.BOLD = ''
        self.ITAL = ''
        self.UNDER = ''
        self.SWAP = ''
        self.ENDC = ''