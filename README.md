# sqlite-ansible

This is a sqlite module for ansible. 
It can create one or more database files, delete them, dump them and execute sqlite queries.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

On nodes:

* python3
```sh
apt install python3
```

### Installation

1. Clone the repo
```sh
git clone https://github.com/zedatav/sqlite-ansible
```

2. Import the module

copy or move the [sqlite.py](sqlite.py) file in /etc/ansible/library
```sh
mv sqlite.py /etc/ansible/library
```

## Usage

Using it in a [role](https://galaxy.ansible.com/docs/contributing/creating_role.html) following the examples in [sqlite.py](sqlite.py) and execute a [playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html) with the defined role inside. Or use it directly in a playbook.

For examples and doc:
```sh
ansible-doc -M library sqlite
```
## Authors

ZedAtav

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details
