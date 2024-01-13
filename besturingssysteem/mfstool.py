###################################################
# name     : Luuk van der Waals                   #
# UvAnetID : 13309900                             #
# Study    : BCs Informatica                      #
#                                                 #
# This program can execute commands to work       #
# with the minix filesystem.                      #
#                                                 #
# Usage: Usage: mfstool.py image command params   #
###################################################

import sys
import struct
import time

BLOCK_SIZE = 1024
INODE_SIZE = 32
MINIX_SUPER_MAGIC = 0x137F
MINIX_SUPER_MAGIC2 = 0x138F
N_ZONES = 9
S_IFREG = 0o100000
S_IFDIR = 0o040000
MODE_TYPE_BITS = 0o170000


# Parse functions #


def parse_superblock(data):
    """
    Reads the bytes of a superBlock. Returns a dictionary containing the super
    block elements.
    """

    superBlock = {}

    idx = 0
    (superBlock["ninodes"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (superBlock["nzones"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (superBlock["imap"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (superBlock["zmap"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (superBlock["firstdatazone"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (superBlock["logzonesize"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (superBlock["maxfilezise"],) = struct.unpack("<L", data[idx:idx+4])
    idx += 4
    (superBlock["minixmagic"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (superBlock["mountstate"],) = struct.unpack("<H", data[idx:idx+2])

    return superBlock


def parse_inode(n):
    """
    Reads the byte of a inode. Returns a dictionary containing the elements
    of the inode.
    """

    data = inbytes[(n - 1) * INODE_SIZE:n * INODE_SIZE]

    inode = {}

    idx = 0
    (inode["i_mode"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (inode["i_uid"],) = struct.unpack("<H", data[idx:idx+2])
    idx += 2
    (inode["i_size"],) = struct.unpack("<L", data[idx:idx+4])
    idx += 4
    (inode["i_time"],) = struct.unpack("<L", data[idx:idx+4])
    idx += 4
    (inode["i_gid"],) = struct.unpack("<B", data[idx:idx+1])
    idx += 1
    (inode["i_nlinks"],) = struct.unpack("<B", data[idx:idx+1])
    idx += 1
    i_nzone = []
    for i in range(N_ZONES):
        (zone,) = struct.unpack("<H", data[idx:idx+2])
        i_nzone.append(zone)
        idx += 2
    inode["i_nzone"] = i_nzone

    return inode


# Manage zones #


def create_zone():
    """
    Finds a free zone and change the corresponding bit in the imap to a 1.
    Returns the address of the newly occupied zone.
    """

    # Find a byte containing 0.
    idx = 0
    while zmbytes[idx] == 255:
        idx += 1

    byte = bin(zmbytes[idx])[2:]

    # Find the 0 in the byte and change it to a 1.
    bit = len(byte) - byte.rfind('0')
    zmbytes[idx] = zmbytes[idx] + 2 ** (bit - 1)

    # Calculate and return the address of the new zone.
    return idx * 8 + bit + superBlock["firstdatazone"] - 2


def read_indirect_pointer(zone, idx):
    """
    Returns the address at the position of idx in an indirect pointer.
    """

    i = (zone - superBlock["firstdatazone"]) * BLOCK_SIZE

    idx = (zone - superBlock["firstdatazone"]) * BLOCK_SIZE + idx * 2
    (zone,) = struct.unpack("<H", datazones[idx:idx + 2])

    return zone


def add_zone(inode):
    """
    Add a new zone to a file.
    """

    inode, inodeAddress = inode
    nzone = int(inode["i_size"] / BLOCK_SIZE)

    if nzone <= 7:
        # Add zone to the direct pointers.
        idx = (inodeAddress - 1) * INODE_SIZE + 14 + nzone * 2
        address = create_zone()
        inbytes[idx:idx + 2] = struct.pack("<H", address)
        if nzone == 7:
            # Create new indirect pointer.
            idx = (address - superBlock["firstdatazone"]) * BLOCK_SIZE
            address = create_zone()
            datazones[idx:idx + 2] = struct.pack("<H", address)
        return address

    nzone -= 7
    if nzone < BLOCK_SIZE / 2:
        # Add zone to indirect pointer.
        idx = (inode["i_nzone"][7] - superBlock["firstdatazone"]) * \
            BLOCK_SIZE + nzone * 2
        address = create_zone()
        datazones[idx:idx + 2] = struct.pack("<H", address)
        return address

    nzone -= BLOCK_SIZE / 2
    if nzone == 0:
        # Create new double indirect pointer.
        idx = (inodeAddress - 1) * INODE_SIZE + 30
        address = create_zone()
        inbytes[idx:idx + 2] = struct.pack("<H", address)
    else:
        address = inode["i_nzone"][8]

    if nzone % (BLOCK_SIZE / 2) == 0:
        # Create new indirect pointer in indirect pointer.
        idx = int((address - superBlock["firstdatazone"]) * BLOCK_SIZE + \
            nzone / (BLOCK_SIZE / 2) * 2)
        address = create_zone()
        datazones[idx:idx + 2] = struct.pack("<H", address)
    else:
        address = read_indirect_pointer(address, int(nzone / (BLOCK_SIZE / 2)))

    # Add zone to the indirect pointer.
    nzone %= (BLOCK_SIZE / 2)
    idx = int((address - superBlock["firstdatazone"]) * BLOCK_SIZE + nzone * 2)
    address = create_zone()
    datazones[idx:idx + 2] = struct.pack("<H", address)

    return address


def get_zone(nzone, inode):
    """
    Get the nth zone of a file.
    """

    if nzone < 7:
        # Get direct pointer.
        return inode["i_nzone"][nzone]

    nzone -= 7
    if nzone < BLOCK_SIZE / 2:
        # Get indirect pointer.
        if inode["i_nzone"][7] == 0:
            return 0

        return read_indirect_pointer(inode["i_nzone"][7], nzone)

    # Get double indirect pointer.
    nzone -= int(BLOCK_SIZE / 2)
    if inode["i_nzone"][8] == 0:
        return 0

    zone = read_indirect_pointer(inode["i_nzone"][8],
        int(nzone / (BLOCK_SIZE / 2)))

    return read_indirect_pointer(zone, int(nzone % (BLOCK_SIZE / 2)))


def get_zones(inode):
    """
    Returns a generate that contains all zones off a zone.
    """

    if inode["i_size"] == 0:
        return

    nzones = int((inode["i_size"] - 1) / BLOCK_SIZE) + 1

    for i in range(nzones):
        yield get_zone(i, inode)


# Other auxiliary functions #


def find_file(path, returnAddress = False):
    """
    Finds a file through a path. Returns the inode of the file. Also returns
    the address of the inode in case returnAddress is true.
    """

    global inode
    path = bytearray(path.encode()).split(b'/')
    inode = rootInode

    for filename in path:
        if not filename:
            continue

        if not inode:
            sys.exit(-1)

        # Find the zone of dictionary.
        idx = inode["i_nzone"][0] - superBlock["firstdatazone"]
        size = inode["i_size"]
        datazone = datazones[idx * BLOCK_SIZE:(idx + 1) * BLOCK_SIZE]

        # Search for the filename in the dictionary and take corresponding
        # address of inode.
        inode = None
        for i in range(0, size, 2 + name_length):
            if datazone[i + 2:i + 2 + name_length].rstrip(b'\0') == filename:
                (address,) = struct.unpack("<H", datazone[i:i + 2])
                inode = parse_inode(address)
                break

    return (inode, address) if returnAddress else inode


def create_inode(mode):
    """
    Finds a free zone and change the corresponding bit in the imap to a 1.
    Returns the address of the newly occupied zone.
    """

    # Find a byte containing a 0.
    idx = 0
    while imbytes[idx] == 255:
        idx += 1

    # Find a 0 in the byte and change it to 1.
    byte = bin(imbytes[idx])[2:]
    bit = len(byte) - byte.rfind('0')

    imbytes[idx] = imbytes[idx] + 2 ** (bit - 1)

    # Calculate the address of the new inode.
    address = idx * 8 + bit - 1

    inode = bytearray(INODE_SIZE)
    idx = 0
    # i_moode
    inode[idx:idx + 2] = struct.pack("<H", mode)
    idx += 2
    # i_uid
    inode[idx:idx + 2] = struct.pack("<H", 0)
    idx += 2
    # i_size
    inode[idx:idx + 4] = struct.pack("<L", 0)
    idx += 4
    # i_time
    inode[idx:idx + 4] = struct.pack("<L", int(time.time()))
    idx += 4
    # i_gid
    inode[idx:idx + 1] = struct.pack("<B", 0)
    idx += 1
    # i_nlinks
    inode[idx:idx + 1] = struct.pack("<B", 1)
    idx += 1
    # i_nzones
    for i in range(N_ZONES):
        inode[idx:idx + 2] = struct.pack("<H", 0)
        idx += 2

    inbytes[(address - 1) * INODE_SIZE:address * INODE_SIZE] = inode

    return address


def create_file(mode):
    """
    Creates a new file in the file system. Returns the address of the inode
    corresponding to the new file. Returns the address of the new inode.
    """

    if len(sys.argv) <= 3:
        sys.stderr.buffer.write(b'Argument missing\n')
        sys.exit(-1)

    argv = sys.argv[3]

    # find the directory in which the file will be created.
    if argv.rfind('/') == -1:
        inode = (rootInode, 1)
    else:
        path = argv[:argv.rfind('/')]
        inode = find_file(path, True)

    # Create a new inode and add the address of the inode and filename to the
    # directory.
    filename = argv[argv.rfind('/') + 1:]
    newInode = create_inode(mode)

    content = struct.pack("<H", newInode) + bytearray(filename.encode()) + \
        bytes(name_length - len(filename))
    add_content(inode, content)

    return newInode


def add_content(inode, content):
    """
    Adds any kind of content to a file.
    """

    (inode, inodeAddress) = inode

    # Divide the new content the over zones.
    contentList = [content[:BLOCK_SIZE - (inode["i_size"] % BLOCK_SIZE)]]
    content = content[BLOCK_SIZE - (inode["i_size"] % BLOCK_SIZE):]
    while not content == b'':
        contentList.append(content[:BLOCK_SIZE])
        content = content[BLOCK_SIZE:]

    for content in contentList:
        inode = parse_inode(inodeAddress)

        # Find zone to add content to or add zone in case all zones are full.
        nzone = int(inode["i_size"] / BLOCK_SIZE)
        zone = get_zone(nzone, inode)
        if zone == 0:
            zone = add_zone((inode, inodeAddress))

        # Add the content to the zone.
        idx = (zone - superBlock["firstdatazone"]) * BLOCK_SIZE + \
            inode["i_size"] % BLOCK_SIZE
        datazones[idx:idx + len(content)] = content

        # Change the size of the file.
        idx = (inodeAddress - 1) * INODE_SIZE + 4
        inbytes[idx:idx + 4] = struct.pack("<L", inode["i_size"] + len(content))


# Commands #


def ls():
    """
    Lists all the file in a directory.
    """

    # Find the directory.
    if len(sys.argv) <= 3:
        inode = rootInode
    else:
        inode = find_file(sys.argv[3])

    if not inode:
        sys.stderr.buffer.write(bytearray(sys.argv[3].encode()) +
                                b' not found\n')
        sys.exit(-1)

    if not inode["i_mode"] & MODE_TYPE_BITS == S_IFDIR:
        sys.stderr.buffer.write(b'Not a directory\n')
        sys.exit(-1)

    size = BLOCK_SIZE

    for i, zone in enumerate(get_zones(inode)):
        zone -= superBlock["firstdatazone"]
        datazone = datazones[zone * BLOCK_SIZE:(zone + 1) * BLOCK_SIZE]

        # In case of last zone, calculate the used size of the zone.
        if inode["i_size"] - i * BLOCK_SIZE < BLOCK_SIZE:
            size = inode["i_size"] - i * BLOCK_SIZE

        # Print the filename in the directory.
        for j in range(0, size, 2 + name_length):
            printname = datazone[j + 2:j + 2 + name_length].rstrip(b'\0')
            sys.stdout.buffer.write(printname + b'\n')


def cat():
    """
    Prints the contents of a text file.
    """

    if len(sys.argv) <= 3:
        sys.stderr.buffer.write(b'Argument missing\n')
        sys.exit(-1)

    inode = find_file(sys.argv[3])

    # File not found.
    if not inode:
        sys.stderr.buffer.write(bytearray(sys.argv[3].encode()) +
                                b' not found\n')
        sys.exit(-1)

    if inode["i_mode"] & MODE_TYPE_BITS != S_IFREG:
        sys.stderr.buffer.write(bytearray(sys.argv[3].encode()) + b' is not a text file\n')
        sys.exit(-1)

    # Print the file
    size = inode["i_size"]
    for zone in get_zones(inode):
        zone -= superBlock["firstdatazone"]
        datazone = datazones[zone * BLOCK_SIZE:(zone + 1) * BLOCK_SIZE].rstrip(b'\0')
        sys.stdout.buffer.write(datazone)


def touch():
    """
    Creates a new text file.
    """

    create_file(0o100700)


def mkdir():
    """
    Creates a new directory.
    """

    if len(sys.argv) <= 3:
        sys.stderr.buffer.write(b'Argument missing\n')
        sys.exit(-1)

    argv = sys.argv[3]

    # Find the address of the parent directory.
    if argv.rfind('/') == -1:
        parentAddress = 1
    else:
        path = argv[:argv.rfind('/')]
        (_, parentAddress) = find_file(path, True)

    # Create the directory.
    inodeAddress = create_file(0o40700)
    inode = (parse_inode(inodeAddress), inodeAddress)

    # Add the "." and ".." files to the directory.
    content = struct.pack("<H", inodeAddress) + b'.' + bytes(name_length - 1) \
        + struct.pack("<H", parentAddress) + b'..' + bytes(name_length - 2)
    add_content(inode, content)


def append():
    """
    Append content to a text file.
    """

    if len(sys.argv) <= 4:
        sys.stderr.buffer.write(b'Arguments missing\n')
        sys.exit(-1)

    inode = find_file(sys.argv[3], True)
    content = bytearray(sys.argv[4].encode())
    add_content(inode, content)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: mfstool.py image command params")
        sys.exit(-1)

    diskimg = sys.argv[1]
    cmd = sys.argv[2]

    with open(diskimg, "rb") as f:
        bootBlock = f.read(BLOCK_SIZE)

        # Read the super block.
        sbbytes = f.read(BLOCK_SIZE)
        superBlock = parse_superblock(sbbytes)

        # Determine the length of the file names.
        if superBlock["minixmagic"] == MINIX_SUPER_MAGIC:
            name_length = 14
        elif superBlock["minixmagic"] == MINIX_SUPER_MAGIC2:
            name_length = 30

        # Read the maps
        imbytes = bytearray(f.read(superBlock["imap"] * BLOCK_SIZE))
        zmbytes = bytearray(f.read(superBlock["zmap"] * BLOCK_SIZE))

        # Read the inode table.
        n = int(superBlock["ninodes"] * 32 / BLOCK_SIZE)
        inbytes = bytearray(f.read(n * BLOCK_SIZE))
        rootInode = parse_inode(1)

        # Read the datazones.
        datazones = bytearray(f.read())

    # Handle the command.
    if cmd == "ls":
        ls()
    elif cmd == "cat":
        cat()
    elif cmd == "touch":
        touch()
    elif cmd == "mkdir":
        mkdir()
    elif cmd == "append":
        append()

    # Write the new data to the disk image.
    newdata = bootBlock + sbbytes + imbytes + zmbytes + inbytes + datazones

    with open(diskimg, "wb") as f:
        f.write(newdata)
